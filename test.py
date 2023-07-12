import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from camera import Camera
import obj
import pyrr

cam = Camera()

def key_input(window, key, scancode, action, mode):
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    if key == glfw.KEY_W and action == glfw.PRESS:
        cam.pos += cam.front * cam.velocity
    elif key == glfw.KEY_S and action == glfw.PRESS:
        cam.pos -= cam.front * cam.velocity
    elif key == glfw.KEY_A and action == glfw.PRESS:
        cam.pos += cam.left * cam.velocity
    elif key == glfw.KEY_D and action == glfw.PRESS:
        cam.pos -= cam.left * cam.velocity
    elif key == glfw.KEY_R and action == glfw.PRESS:
        cam.pos += cam.up * cam.velocity
    elif key == glfw.KEY_F and action == glfw.PRESS:
        cam.pos -= cam.up * cam.velocity
    elif key == glfw.KEY_UP and action == glfw.PRESS:
        cam.rotate_pitch(5.0)
    elif key == glfw.KEY_DOWN and action == glfw.PRESS:
        cam.rotate_pitch(-5.0)
    elif key == glfw.KEY_LEFT and action == glfw.PRESS:
        cam.rotate_yaw(5.0)
    elif key == glfw.KEY_RIGHT and action == glfw.PRESS:
        cam.rotate_yaw(-5.0)
    elif key == glfw.KEY_Q and action == glfw.PRESS:
        cam.rotate_roll(5.0)
    elif key == glfw.KEY_E and action == glfw.PRESS:
        cam.rotate_roll(-5.0)


def main():
    if not glfw.init():
        print("Cannot initialize GLFW")
        exit()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    WIDTH, HEIGHT = 1280, 720
    window = glfw.create_window(WIDTH, HEIGHT, "OpenGL window", None, None)
    if not window:
        glfw.terminate()
        print("GLFW window cannot be created")
        exit()
    glfw.set_window_pos(window, 100, 100)
    glfw.set_key_callback(window, key_input)
    glfw.make_context_current(window)

    positions = np.array(obj.position, dtype=np.float32)
    normals = np.array(obj.normal, dtype=np.float32)
    indices = np.array(obj.indice, dtype=np.uint32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)
    glBindVertexArray(VAO)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, positions.nbytes + normals.nbytes, None, GL_DYNAMIC_DRAW)
    glBufferSubData(GL_ARRAY_BUFFER, 0, positions.nbytes, positions)
    glBufferSubData(GL_ARRAY_BUFFER, positions.nbytes, normals.nbytes, normals)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, False, 12, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, False, 12, ctypes.c_void_p(positions.nbytes))

    vs = open("shaders/shader.vs", "r")
    fs = open("shaders/shader.fs", "r")
    shader = compileProgram(compileShader(vs.read(), GL_VERTEX_SHADER), compileShader(fs.read(), GL_FRAGMENT_SHADER))
    glUseProgram(shader)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        projection = pyrr.matrix44.create_perspective_projection_matrix(cam.fov, WIDTH / HEIGHT, cam.near, cam.far)
        view = pyrr.matrix44.create_look_at(cam.pos, cam.pos + cam.front, cam.up)
        model = pyrr.matrix44.create_identity()

        glUniformMatrix4fv(glGetUniformLocation(shader, "projection"), 1, GL_FALSE, projection)
        glUniformMatrix4fv(glGetUniformLocation(shader, "view"), 1, GL_FALSE, view)
        glUniformMatrix4fv(glGetUniformLocation(shader, "model"), 1, GL_FALSE, model)
        glUniform3fv(glGetUniformLocation(shader, "lightPos"), 1, pyrr.Vector3([0.0, 2.0, 2.0]))
        glUniform3fv(glGetUniformLocation(shader, "viewPos"), 1, cam.pos)

        # glDrawArrays(GL_TRIANGLES, 0, len(indices))
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
        
        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == '__main__':
    main()