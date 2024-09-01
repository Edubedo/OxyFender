import pygame
from general.settings import *

from game_levels.beginner.level1.level1 import Level1Beginner
from game_levels.beginner.level2.level2 import Level2Beginner
from game_levels.beginner.level3.level3 import Level3Beginner

from game_levels.advanced.level1.level1 import Level1Advanced
from game_levels.advanced.level2.level2 import Level2Advanced
from game_levels.advanced.level3.level3 import Level3Advanced

class MenuGame:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.font = pygame.font.Font(None, 36)

    def show_difficulty_menu(self):
        self.screen.fill(BACKGROUND_COLOR)

        if self.config.get_language() == "english":
            difficulty_options = [
                {
                "name" : "Beginner",
                "id": "beginner"
                },
                {
                "name" : "Advanced",
                "id": "advanced"
                }
            ] 
        else: 
            difficulty_options = [
                {
                "name" : "Principiante",
                "id": "beginner"
                },
                {
                "name" : "Avanzado",
                "id": "advanced"
                }
            ] 
        
        self.options_difficult = []  

        for i, difficulty in enumerate(difficulty_options):
            text = self.font.render(difficulty['name'], True, TEXT_COLOR)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 150 + i * 50))
            self.screen.blit(text, rect)
            self.options_difficult.append((difficulty, rect))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for difficulty, rect in self.options_difficult:
                        if rect.collidepoint(event.pos):
                            return self.show_level_menu(difficulty)

    def show_level_menu(self, difficulty):
        self.screen.fill(BACKGROUND_COLOR)
        level_options = []

        for i in range(1, 4):
            level_options.append({
                "name": f"Level {i}",
                "difficulty": difficulty['name'],
                "id": f"{difficulty['id'].lower()}_level_{i}"
            })

        self.option_rects = []  
        for i, level in enumerate(level_options):
            text = self.font.render(level['name'], True, TEXT_COLOR)
            rect = text.get_rect(center=(self.screen.get_width() // 2, 150 + i * 50))
            self.screen.blit(text, rect)
            self.option_rects.append((level, rect))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for level, rect in self.option_rects:
                        if rect.collidepoint(event.pos):

                           # Levels for the beginner 
                           if level['id'] == "beginner_level_1":
                                Level1Beginner(level['name'], level['difficulty'], level['id']).run()
                           if level['id'] == "beginner_level_2":
                                Level2Beginner(level['name'], level['difficulty'], level['id'])
                           if level['id'] == "beginner_level_3":
                                Level3Beginner(level['name'], level['difficulty'], level['id'])
                           
                           # Levels for the advanced 
                           if level['id'] == "advanced_level_1":
                                Level1Advanced(level['name'], level['difficulty'], level['id'])
                           if level['id'] == "advanced_level_2":
                                Level2Advanced(level['name'], level['difficulty'], level['id'])
                           if level['id'] == "advanced_level_3":
                                Level3Advanced(level['name'], level['difficulty'], level['id'])