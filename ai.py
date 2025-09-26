import pygame
import numpy as np
import random
import copy


# Neural network that takes 3 inputs (bird y, pipe x, pipe gap y) and produces one output.
class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_hidden = np.random.randn(hidden_size)
        self.bias_output = np.random.randn(output_size)

    def forward(self, inputs):
        hidden_layer = np.tanh(np.dot(inputs, self.weights_input_hidden) + self.bias_hidden)
        output_layer = np.tanh(np.dot(hidden_layer, self.weights_hidden_output) + self.bias_output)
        return output_layer

    def mutate(self, mutation_rate=0.1):
        def mutate_weights(weights):
            for i in range(weights.shape[0]):
                for j in range(weights.shape[1]):
                    if random.random() < mutation_rate:
                        weights[i, j] += np.random.randn() * 0.5

        mutate_weights(self.weights_input_hidden)
        mutate_weights(self.weights_hidden_output)
        self.bias_hidden += np.random.randn(self.hidden_size) * mutation_rate
        self.bias_output += np.random.randn(self.output_size) * mutation_rate


# Bird that uses a neural network to decide when to flap.
class Bird:
    def __init__(self):
        self.x = 100  # Fixed horizontal position
        self.y = 300
        self.velocity = 0
        self.gravity = 0.6
        self.lift = -10
        self.nn = NeuralNetwork(3, 5, 1)
        self.score = 0
        self.alive = True

    def update(self):
        if self.alive:
            self.velocity += self.gravity
            self.y += self.velocity
            self.score += 1
            # Kill bird if it goes off-screen
            if self.y > 600 or self.y < 0:
                self.alive = False

    def flap(self):
        self.velocity += self.lift

    def decide(self, pipe_x, pipe_gap_y):
        # Normalize inputs (bird y, pipe x, and pipe gap y)
        inputs = np.array([self.y / 600, pipe_x / 800, pipe_gap_y / 600])
        output = self.nn.forward(inputs)
        # Extract the scalar from the 1-element output array
        if output[0] > 0:
            self.flap()

    def mutate(self):
        self.nn.mutate()


# Genetic algorithm that evolves the birds’ neural networks.
class GeneticAlgorithm:
    def __init__(self, population_size=50):
        self.population_size = population_size
        self.birds = [Bird() for _ in range(population_size)]

    def evolve(self):
        # Sort birds by score (highest first)
        self.birds.sort(key=lambda bird: bird.score, reverse=True)
        print("Best score this generation:", self.birds[0].score)
        top_performers = self.birds[:10]
        new_birds = []
        for i in range(self.population_size):
            parent = random.choice(top_performers)
            child = Bird()
            # Deep copy the parent's neural network before mutating
            child.nn = copy.deepcopy(parent.nn)
            child.mutate()
            new_birds.append(child)
        self.birds = new_birds


# Main game loop where the AI-controlled birds try to navigate through pipes.
def run_ai_game():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Flappy Bird AI")
    clock = pygame.time.Clock()

    # Initialize genetic algorithm and generation count
    ga = GeneticAlgorithm(population_size=50)
    generation = 1

    # Pipe properties
    pipe_width = 50
    pipe_gap_size = 150
    pipe_x = screen_width
    pipe_speed = 3
    pipe_gap_y = random.randint(pipe_gap_size // 2 + 10, screen_height - pipe_gap_size // 2 - 10)

    running = True
    while running:
        clock.tick(60)  # 60 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move the pipe leftwards; reset when it goes off-screen.
        pipe_x -= pipe_speed
        if pipe_x < -pipe_width:
            pipe_x = screen_width
            pipe_gap_y = random.randint(pipe_gap_size // 2 + 10, screen_height - pipe_gap_size // 2 - 10)

        # Update and let each bird make its decision.
        all_dead = True
        for bird in ga.birds:
            if bird.alive:
                all_dead = False
                bird.decide(pipe_x, pipe_gap_y)
                bird.update()
                # Check for collision with the pipe.
                if pipe_x < bird.x < pipe_x + pipe_width:
                    if bird.y < pipe_gap_y - pipe_gap_size // 2 or bird.y > pipe_gap_y + pipe_gap_size // 2:
                        bird.alive = False

        # If all birds have died, evolve to the next generation.
        if all_dead:
            ga.evolve()
            generation += 1
            # Reset birds for the new generation.
            for bird in ga.birds:
                bird.y = 300
                bird.velocity = 0
                bird.score = 0
                bird.alive = True
            # Reset the pipe.
            pipe_x = screen_width
            pipe_gap_y = random.randint(pipe_gap_size // 2 + 10, screen_height - pipe_gap_size // 2 - 10)

        # Draw background.
        screen.fill((0, 0, 0))

        # Draw the pipe (upper and lower parts).
        pygame.draw.rect(screen, (0, 255, 0), (pipe_x, 0, pipe_width, pipe_gap_y - pipe_gap_size // 2))
        pygame.draw.rect(screen, (0, 255, 0), (
        pipe_x, pipe_gap_y + pipe_gap_size // 2, pipe_width, screen_height - (pipe_gap_y + pipe_gap_size // 2)))

        # Draw each bird (alive birds in white, dead birds in red).
        for bird in ga.birds:
            color = (255, 255, 255) if bird.alive else (255, 0, 0)
            pygame.draw.circle(screen, color, (int(bird.x), int(bird.y)), 5)

        # Display generation info.
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(f"Generation: {generation}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    run_ai_game()
