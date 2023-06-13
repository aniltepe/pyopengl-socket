from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

glutInit()

def display():
    glClearColor(1, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glutSwapBuffers()
    glutPostRedisplay()

def main():
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutCreateWindow('window')
    glutDisplayFunc(display)
    glutMainLoop()

if __name__=='__main__':
    main()