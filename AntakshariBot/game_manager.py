import asyncio
import logging
import time
from typing import Dict, List, Optional
from AntakshariBot.database import db
from AntakshariBot.word_validator import WordValidator
import config

logger = logging.getLogger(__name__)

class GameManager:
    def __init__(self):
        self.active_games: Dict[int, dict] = {}
        self.join_timers: Dict[int, asyncio.Task] = {}
        self.turn_timers: Dict[int, asyncio.Task] = {}
        self.word_validator = WordValidator()
    
    async def start_game(self, chat_id: int, user_id: int, user_name: str) -> dict:
        """Start a new game in the chat"""
        try:
            if chat_id in self.active_games:
                return {"success": False, "message": "A game is already active in this group!"}
            
            # Create new game
            game_data = {
                "chat_id": chat_id,
                "status": "joining",
                "players": [{"id": user_id, "name": user_name, "score": 0, "streak": 0}],
                "current_player": 0,
                "last_word": "",
                "next_letter": "",
                "used_words": set(),
                "round": 0,
                "max_rounds": 50,
                "start_time": time.time(),
                "creator": user_id
            }
            
            self.active_games[chat_id] = game_data
            
            # Save to database
            await db.create_game(game_data)
            
            return {"success": True, "game": game_data}
            
        except Exception as e:
            logger.error(f"Error starting game: {e}")
            return {"success": False, "message": "Failed to start game. Please try again."}
    
    async def join_game(self, chat_id: int, user_id: int, user_name: str) -> dict:
        """Join an existing game"""
        try:
            if chat_id not in self.active_games:
                return {"success": False, "message": "No active game in this group!"}
            
            game = self.active_games[chat_id]
            
            if game["status"] != "joining":
                return {"success": False, "message": "Game has already started!"}
            
            # Check if user already joined
            for player in game["players"]:
                if player["id"] == user_id:
                    return {"success": False, "message": "You have already joined this game!"}
            
            # Check max players
            if len(game["players"]) >= config.MAX_PLAYERS:
                return {"success": False, "message": f"Game is full! Maximum {config.MAX_PLAYERS} players allowed."}
            
            # Add player
            game["players"].append({"id": user_id, "name": user_name, "score": 0, "streak": 0})
            
            # Update database
            await db.update_game(chat_id, game)
            
            return {"success": True, "game": game}
            
        except Exception as e:
            logger.error(f"Error joining game: {e}")
            return {"success": False, "message": "Failed to join game. Please try again."}
    
    async def leave_game(self, chat_id: int, user_id: int) -> dict:
        """Leave the current game"""
        try:
            if chat_id not in self.active_games:
                return {"success": False, "message": "No active game in this group!"}
            
            game = self.active_games[chat_id]
            
            # Find and remove player
            for i, player in enumerate(game["players"]):
                if player["id"] == user_id:
                    game["players"].pop(i)
                    
                    # Adjust current player index if needed
                    if game["status"] == "active" and i <= game["current_player"]:
                        game["current_player"] = max(0, game["current_player"] - 1)
                    
                    # End game if not enough players
                    if len(game["players"]) < config.MIN_PLAYERS:
                        await self.end_game(chat_id)
                        return {"success": True, "message": "Game ended due to insufficient players."}
                    
                    # Update database
                    await db.update_game(chat_id, game)
                    return {"success": True}
            
            return {"success": False, "message": "You are not in this game!"}
            
        except Exception as e:
            logger.error(f"Error leaving game: {e}")
            return {"success": False, "message": "Failed to leave game. Please try again."}
    
    async def start_join_timer(self, chat_id: int, client):
        """Start the join timer for a game"""
        try:
            await asyncio.sleep(config.JOIN_TIME)
            
            if chat_id in self.active_games:
                game = self.active_games[chat_id]
                
                if game["status"] == "joining":
                    if len(game["players"]) >= config.MIN_PLAYERS:
                        # Start the game
                        game["status"] = "active"
                        game["round"] = 1
                        
                        await db.update_game(chat_id, game)
                        
                        current_player = game["players"][game["current_player"]]
                        
                        await client.send_message(
                            chat_id,
                            f"🎮 **Game Started!**\n\n"
                            f"👥 **Players:** {len(game['players'])}\n"
                            f"🎯 **First Turn:** {current_player['name']}\n"
                            f"🌍 **Say any country or city name to begin!**\n"
                            f"⏰ You have {config.TURN_TIME} seconds per turn"
                        )
                        
                        # Start turn timer
                        self.turn_timers[chat_id] = asyncio.create_task(
                            self.turn_timeout(chat_id, client)
                        )
                    else:
                        # Not enough players
                        await self.end_game(chat_id)
                        await client.send_message(
                            chat_id,
                            f"❌ **Game Cancelled**\n\n"
                            f"Not enough players joined. Minimum {config.MIN_PLAYERS} players required."
                        )
            
        except Exception as e:
            logger.error(f"Error in join timer: {e}")
    
    async def process_word(self, chat_id: int, user_id: int, user_name: str, word: str) -> dict:
        """Process a word submission"""
        try:
            if chat_id not in self.active_games:
                return {"success": False, "error": False}
            
            game = self.active_games[chat_id]
            
            if game["status"] != "active":
                return {"success": False, "error": False}
            
            # Check if it's the player's turn
            current_player = game["players"][game["current_player"]]
            if current_player["id"] != user_id:
                return {"success": False, "error": True, "message": f"It's {current_player['name']}'s turn!"}
            
            # Validate word
            validation_result = await self.word_validator.validate_word(
                word, game["next_letter"], game["used_words"]
            )
            
            if not validation_result["valid"]:
                # Wrong answer - eliminate player
                await self.eliminate_player(chat_id, user_id)
                return {"success": False, "error": True, "message": validation_result["reason"], "eliminated": True}
            
            # Correct answer
            points = config.POINTS_PER_WORD
            
            # Add bonus points for rare words
            if validation_result.get("rare", False):
                points += config.BONUS_POINTS
            
            # Add streak bonus
            current_player["streak"] += 1
            if current_player["streak"] > 1:
                points += current_player["streak"] - 1
            
            current_player["score"] += points
            
            # Add word to used words
            game["used_words"].add(word.lower())
            game["last_word"] = word.title()
            game["next_letter"] = word[-1].lower()
            
            # Update player stats
            await db.update_player_stats(user_id, user_name, "correct_word", points)
            
            # Check win condition
            if current_player["score"] >= 100 or game["round"] >= game["max_rounds"]:
                return await self.end_game_with_winner(chat_id)
            
            # Move to next turn
            await self.next_turn(chat_id)
            
            # Update database
            await db.update_game(chat_id, game)
            
            # Cancel current turn timer and start new one
            if chat_id in self.turn_timers:
                self.turn_timers[chat_id].cancel()
            
            # Don't start new timer if game ended
            if chat_id in self.active_games:
                self.turn_timers[chat_id] = asyncio.create_task(
                    self.turn_timeout(chat_id, None)
                )
            
            next_player = game["players"][game["current_player"]]
            
            return {
                "success": True,
                "type": "correct",
                "points": points,
                "streak": current_player["streak"],
                "next_letter": game["next_letter"],
                "next_player": next_player["name"]
            }
            
        except Exception as e:
            logger.error(f"Error processing word: {e}")
            return {"success": False, "error": True, "message": "An error occurred. Please try again."}
    
    async def eliminate_player(self, chat_id: int, user_id: int):
        """Eliminate a player from the game"""
        if chat_id in self.active_games:
            game = self.active_games[chat_id]
            
            # Find and remove the player
            for i, player in enumerate(game["players"]):
                if player["id"] == user_id:
                    eliminated_player = game["players"].pop(i)
                    
                    # Adjust current player index if needed
                    if i <= game["current_player"]:
                        game["current_player"] = max(0, game["current_player"] - 1)
                    
                    # Check if only one player remains
                    if len(game["players"]) == 1:
                        # Last player wins
                        winner = game["players"][0]
                        await self.declare_winner(chat_id, winner)
                    elif len(game["players"]) == 0:
                        # No players left, end game
                        await self.end_game(chat_id)
                    else:
                        # Continue with next player
                        if game["current_player"] >= len(game["players"]):
                            game["current_player"] = 0
                
                break
    
    async def declare_winner(self, chat_id: int, winner: dict):
        """Declare the winner and end the game"""
        if chat_id in self.active_games:
            game = self.active_games[chat_id]
        
            # Update player stats
            for player in game["players"]:
                is_winner = player["id"] == winner["id"]
                await db.update_player_stats(
                    player["id"], 
                    player["name"], 
                    "game_finished", 
                    player["score"],
                    is_winner
                )
        
            # End the game
            await self.end_game(chat_id)
        
            return {
                "success": True,
                "type": "game_won",
                "winner": winner,
                "reason": "last_player"
            }
    
    async def next_turn(self, chat_id: int):
        """Move to the next player's turn"""
        if chat_id in self.active_games:
            game = self.active_games[chat_id]
            game["current_player"] = (game["current_player"] + 1) % len(game["players"])
            game["round"] += 1
    
    async def turn_timeout(self, chat_id: int, client):
        """Handle turn timeout - eliminate player"""
        try:
            await asyncio.sleep(config.TURN_TIME)
            
            if chat_id in self.active_games:
                game = self.active_games[chat_id]
                current_player = game["players"][game["current_player"]]
            
                # Eliminate the player who timed out
                await self.eliminate_player(chat_id, current_player["id"])
            
                if client and chat_id in self.active_games:
                    remaining_players = len(game["players"])
                    if remaining_players == 1:
                        winner = game["players"][0]
                        await client.send_message(
                            chat_id,
                            f"⏰ **{current_player['name']} eliminated due to timeout!**\n\n"
                            f"🎉 **{winner['name']} wins the game!**\n"
                            f"🏆 **Final Score:** {winner['score']} points"
                        )
                    elif remaining_players > 1:
                        next_player = game["players"][game["current_player"]]
                        await client.send_message(
                            chat_id,
                            f"⏰ **{current_player['name']} eliminated due to timeout!**\n"
                            f"👥 **Players remaining:** {remaining_players}\n"
                            f"🎯 **Next turn:** {next_player['name']}\n"
                            f"📝 **Next letter:** {game['next_letter'].upper() if game['next_letter'] else 'Any'}"
                        )
                    
                        # Start next turn timer
                        self.turn_timers[chat_id] = asyncio.create_task(
                            self.turn_timeout(chat_id, client)
                        )
                    else:
                        await client.send_message(
                            chat_id,
                            f"⏰ **{current_player['name']} eliminated!**\n\n"
                            f"🎮 **Game Over** - No players remaining!"
                        )
            
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Error in turn timeout: {e}")
    
    async def end_game_with_winner(self, chat_id: int) -> dict:
        """End game and declare winner"""
        if chat_id not in self.active_games:
            return {"success": False}
        
        game = self.active_games[chat_id]
        
        # Find winner (highest score)
        winner = max(game["players"], key=lambda p: p["score"])
        
        # Update player stats
        for player in game["players"]:
            is_winner = player["id"] == winner["id"]
            await db.update_player_stats(
                player["id"], 
                player["name"], 
                "game_finished", 
                player["score"],
                is_winner
            )
        
        # Prepare result
        result = {
            "success": True,
            "type": "game_won",
            "winner": winner,
            "scores": {str(p["id"]): p["score"] for p in game["players"]},
            "player_names": {str(p["id"]): p["name"] for p in game["players"]}
        }
        
        # Clean up
        await self.end_game(chat_id)
        
        return result
    
    async def end_game(self, chat_id: int) -> dict:
        """End the current game"""
        try:
            if chat_id in self.active_games:
                # Cancel timers
                if chat_id in self.join_timers:
                    self.join_timers[chat_id].cancel()
                    del self.join_timers[chat_id]
                
                if chat_id in self.turn_timers:
                    self.turn_timers[chat_id].cancel()
                    del self.turn_timers[chat_id]
                
                # Remove from active games
                del self.active_games[chat_id]
                
                # Update database
                await db.end_game(chat_id)
                
                return {"success": True}
            
            return {"success": False, "message": "No active game in this group!"}
            
        except Exception as e:
            logger.error(f"Error ending game: {e}")
            return {"success": False, "message": "Failed to end game."}
    
    async def get_game_info(self, chat_id: int) -> Optional[dict]:
        """Get current game information"""
        if chat_id in self.active_games:
            game = self.active_games[chat_id]
            
            info = {
                "status": game["status"],
                "players": game["players"],
                "round": game.get("round", 0),
                "last_word": game.get("last_word", ""),
                "next_letter": game.get("next_letter", "")
            }
            
            if game["status"] == "active" and game["players"]:
                current_player = game["players"][game["current_player"]]
                info["current_player_name"] = current_player["name"]
            
            return info
        
        return None
