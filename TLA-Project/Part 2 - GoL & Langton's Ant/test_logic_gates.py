# -*- coding: utf-8 -*-
import pygame
import sys
from logic_gates import GliderLogicGates


def visualize_gate(gate_type, input_a, input_b=None):
    pygame.init()
    cell_scale = 15
    grid_size = 40
    screen = pygame.display.set_mode((grid_size * cell_scale, grid_size * cell_scale))
    pygame.display.set_caption(f"Testing {gate_type} Gate | A={input_a}, B={input_b}")
    font = pygame.font.SysFont(None, 22)

    gates = GliderLogicGates()
    if gate_type == "AND":
        gol = gates.setup_and_gate(grid_size, input_a, input_b)
        target_steps = gates._AND_STEPS
        # ناحیه هدف (15, 12) [row, col] که باید بلوک 2x2 در آن تشکیل شود
        # rect بر حسب pygame به صورت (x, y, w, h) است؛ x = ستون * scale, y = سطر * scale
        target_r, target_c = gates._AND_TARGET
        target_rect = (
            (target_c - 1) * cell_scale,
            (target_r - 1) * cell_scale,
            4 * cell_scale,
            4 * cell_scale,
        )
    else:
        gol = gates.setup_not_gate(grid_size, input_a)
        target_steps = gates._NOT_STEPS
        # ناحیه خروجی گیت NOT دقیقاً همان پنجره‌ای است که run_not_gate چک می‌کند
        r_lo, r_hi, c_lo, c_hi = gates._NOT_OUTPUT_WINDOW
        target_rect = (
            c_lo * cell_scale,
            r_lo * cell_scale,
            (c_hi - c_lo) * cell_scale,
            (r_hi - r_lo) * cell_scale,
        )

    clock = pygame.time.Clock()
    running = True
    generation = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # رنگ پس زمینه تیره برای وضوح بیشتر
        screen.fill((30, 30, 30))
        grid = gol.getStates()

        # رسم سلول‌های زنده (رنگ روشن)
        for r in range(grid_size):
            for c in range(grid_size):
                if grid[r, c] == 1:
                    pygame.draw.rect(
                        screen, (200, 255, 200),
                        (c * cell_scale, r * cell_scale, cell_scale - 1, cell_scale - 1),
                    )

        # کادر ناحیه هدف/خروجی: قرمز قبل از رسیدن به نسل تصمیم‌گیری، سبز بعد از آن
        rect_color = (255, 50, 50) if generation < target_steps else (50, 255, 50)
        pygame.draw.rect(screen, rect_color, target_rect, 2)

        # نمایش شماره نسل فعلی و نسل هدف
        label = font.render(f"Gen: {generation} / {target_steps}", True, (255, 255, 255))
        screen.blit(label, (5, 5))

        pygame.display.flip()
        gol.evolve()
        generation += 1
        clock.tick(15)  # سرعت پخش (۱۵ فریم در ثانیه)

    pygame.quit()


if __name__ == "__main__":
    # --- برای تست هر حالت، کافیست علامت کامنت (#) را از ابتدای آن بردارید ---

    # تست‌های گیت AND:
    # visualize_gate("AND", input_a=False, input_b=False)  # خروجی 0 (خالی)
    # visualize_gate("AND", input_a=True, input_b=False)   # خروجی 0 (گلایدر عبور کرده و محو می‌شود)
    # visualize_gate("AND", input_a=False, input_b=True)     # خروجی 0 (گلایدر عبور کرده و محو می‌شود)
    visualize_gate("AND", input_a=True, input_b=True)    # خروجی 1 (تصادم در کادر و تشکیل بلوک)

    # تست‌های گیت NOT:
    # visualize_gate("NOT", input_a=True)
    # visualize_gate("NOT", input_a=False)