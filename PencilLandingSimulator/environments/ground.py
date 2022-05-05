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
        self._agent = agent
        self._running = True

        return self.get_state()

    def get_state(self):
        distanceX = self._goal_pos[0] - self._agent.x
        distanceY = self._goal_pos[1] - self._agent.y
        velocityX = self._agent.dx
        velocityY = self._agent.dy

        return [distanceX, distanceY, velocityX, velocityY]

    def step(self, action):
        # TODO: Process user action in environment

        return self.get_state(), 0, self._running, {}

    def render(self):
        self._window.fill((169, 197, 231))
        image = pygame.transform.rotate(self._agent._image, self._agent.an)
        self._window.blit(image, (self._agent.x, self._agent.y))
        pygame.display.update()
