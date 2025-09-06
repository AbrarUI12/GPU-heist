# hud.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18, glutBitmapCharacter, glutLeaveMainLoop
import sys
import main

# Window size (update if your main window changes)
WIN_W = 1024
WIN_H = 720

def draw_text(x, y, text):
    """Draw text on screen at (x, y) in pixels."""
    glRasterPos2f(x, y)
    for c in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))


def draw_hud(player, health, selected_model):
    """
    Draw player's health as a red bar and ball count as number.
    Exit game if health <= 0.
    """
    # 🔴 Exit game if health runs out
    if health <= 0:
        print("Game Over! Player is dead.")
        try:
            glutLeaveMainLoop()  # clean GLUT exit if available
        except:
            sys.exit(0)          # fallback exit
        return

    # Disable depth and lighting for 2D overlay
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    # Switch to orthographic projection
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # --- Draw Health Bar ---
    bar_width = 300 if selected_model == "Ishrak" else 200
    bar_height = 25
    margin = 20

    # Background (dark gray)
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(margin, WIN_H - margin - bar_height)
    glVertex2f(margin + bar_width, WIN_H - margin - bar_height)
    glVertex2f(margin + bar_width, WIN_H - margin)
    glVertex2f(margin, WIN_H - margin)
    glEnd()

    # ✅ Health fill (red) — proportional to max_health
    health_width = (health / player.max_health) * bar_width
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(margin, WIN_H - margin - bar_height)
    glVertex2f(margin + health_width, WIN_H - margin - bar_height)
    glVertex2f(margin + health_width, WIN_H - margin)
    glVertex2f(margin, WIN_H - margin)
    glEnd()

    # --- Draw Ball Count ---
    glColor3f(1.0, 1.0, 1.0)  # white
    draw_text(margin, WIN_H - margin - bar_height - 30, f"Balls: {player.balls}")

    # Restore matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    # Re-enable depth and lighting
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
