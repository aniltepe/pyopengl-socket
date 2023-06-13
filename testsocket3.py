import socket
import multiprocessing
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import email
from io import StringIO
import time
import json
from types import SimpleNamespace


vertex_src = """
# version 330 core
in vec3 a_position;
void main() {
    gl_Position = vec4(a_position, 1.0);
}
"""

fragment_src = """
# version 330 core
out vec4 out_color;
void main() {
    out_color = vec4(1.0, 0.0, 0.0, 1.0);
}
"""

def start_socket(pipe):
    host = socket.gethostname()
    port = 65432
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(2)
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        data = conn.recv(1024).decode()
        if not data:
            break
        received_body = 0
        _, headers = data.split('\r\n', 1)
        message = email.message_from_file(StringIO(headers.lower()))
        headers = dict(message.items())
        received_body += len(data.split('\r\n\r\n')[1])
        while received_body < int(headers["content-length"]):
            data += conn.recv(1024).decode()
            received_body += 1024

        # with open('requests.txt', 'a') as f:
        #     f.write(data + '\r\n\r\n')

        pipe.send(data.split('\r\n\r\n')[1])
        msg = pipe.recv()
        
        resp = r"""HTTP/1.1 200 OK
Content-Type: text/plain

OK"""
        conn.send(resp.encode())
        conn.close()

def start_scene(pipe):
    while True:
        data = pipe.recv()
        model = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
        start_time = time.time()
        if not glfw.init():
            print("Cannot initialize GLFW")
            exit()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        window = glfw.create_window(320, 240, "OpenGL window", None, None)
        if not window:
            glfw.terminate()
            print("GLFW window cannot be created")
            exit()
        glfw.set_window_pos(window, 100, 100)
        glfw.make_context_current(window)
        vertices = [-0.5, -0.5, 0.0,
                    0.5, -0.5, 0.0,
                    0.0, 0.5, 0.0]
        colors = [1, 0, 0.0, 0.0,
                  0.0, 1.0, 0.0,
                  0.0, 0.0, 1.0]
        vertices = np.array(vertices, dtype=np.float32)
        colors = np.array(colors, dtype=np.float32)

        buff_obj = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, buff_obj)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        shader = compileProgram(compileShader(
            vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
        position = glGetAttribLocation(shader, "a_position")
        glEnableVertexAttribArray(position)
        glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

        glUseProgram(shader)
        glClearColor(0, 0.1, 0.1, 1)

        while not glfw.window_should_close(window):
            curr_time = time.time()
            if curr_time - start_time > 10:
                glfw.set_window_should_close(window, True)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glDrawArrays(GL_TRIANGLES, 0, 3)
            glfw.poll_events()
            glfw.swap_buffers(window)

        glfw.terminate()
        pipe.send(True)

def main():
    conn_endp1, conn_endp2 = multiprocessing.Pipe()
    p1 = multiprocessing.Process(target=start_socket, args=(conn_endp1,))
    p2 = multiprocessing.Process(target=start_scene, args=(conn_endp2,))
    p1.start()
    p2.start()

    p1.join()
    p2.join()
    

if __name__ == '__main__':
    main()