#version 330 core

in vec4 FrontColor;
in vec2 v_texture;

out vec4 FragColor;
uniform sampler2D s_texture;

void main()
{
    FragColor = FrontColor;
}