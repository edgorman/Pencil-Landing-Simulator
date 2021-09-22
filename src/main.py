from SolidGroundEnvironment import SolidGround
import matplotlib.pyplot as plt

if __name__ == "__main__":
    env = SolidGround()
    obs = env.reset()
    screen = env.render(mode = "rgb_array")
    plt.imshow(screen)
    plt.show()
    env.close()
