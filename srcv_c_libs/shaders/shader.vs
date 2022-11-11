#version 330 core

// Input vertex data (different for all executions of this shader)
layout (location = 0) in vec3 vrtx;
layout (location = 1) in vec4 color;
layout(location = 2) in vec2 a_texture;

// Output data (for each fragment)
out vec4 FrontColor;
out vec2 v_texture;

// Constant values for all shader work
uniform mat4 perspective;
uniform mat4 view;
uniform mat4 model;

void main()
{

    gl_Position = perspective * view * model * vec4(vrtx, 1.0f);

    FrontColor = color;
    v_texture = a_texture;
}


