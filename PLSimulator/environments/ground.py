import pygame

from .environment import BaseEnvironment


class GroundEnvironment(BaseEnvironment):
    '''
        GroundEnvironment

        This environment models a simple static ground environment.
    '''

    def __init__(self, goal_pos=(800, 900), width=1600, height=900):
        super().__init__(goal_pos, (10, 10), 2, 10, 9.8, width, height)

    def reset(self, agent):
        self.agent = agent
        self.running = True

        return self.get_state()

    def get_state(self):
        if self.agent is None:
            return []
        
        distanceX = self._goal_pos[0] - self.agent.x
        distanceY = self._goal_pos[1] -  self.agent.y
        velocityX = self.agent.dx
        velocityY = self.agent.dy

        return [distanceX, distanceY, velocityX, velocityY]

    def step(self, action):
        # TODO: Process user action in environment
        #       Should call parent step method to process physics
        #       This level should add anything this specific env models

        return self.get_state(), 0, self.running, {}

    def render(self):
        self.window.fill((169, 197, 231))
        image = pygame.transform.rotate(self.agent.image, self.agent.an)
        self.window.blit(image, (self.agent.x, self.agent.y))
        pygame.display.update()
