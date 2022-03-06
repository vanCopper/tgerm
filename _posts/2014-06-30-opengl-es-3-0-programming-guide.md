---
title: OpenGL ES 3.0 Programming Guide 中文不完全版
tag: [OpenGL]
layout: post
---
**《OpenGL ES 3.0 Programming Guide 中文不完全版》** **看标题有点莫名其妙吗？其实想直接写*xxx中文版*。但由于我并没有逐字翻译和做二次校验，他顶多算是在自己的理解的基础上的二次加工。放到博客一方面是方便查阅，一方面希望能有需要的朋友提供帮助，欢迎*大家来找茬*。把错误留言给我即可，我会第一时间修正。**

另：大家勿要问我要本书英文原版PDF，需要的朋友可至http://www.opengles-book.com购买。

* * *

# 本书目录

*   [OpenGL ES 3.0 简介][1]
*   [Hello Triangle: An OpenGL ES 3.0 Example][2] 
    *   [Code Framework][3]
    *   [Where to Download the Examples][4]
    *   [Hello Triangle Example][5]
    *   [Using the OpenGL ES 3.0 Framework][6]
    *   [Creating a Simple Vertex and Fragment Shader][7]
    *   [Compiling and Loading the Shaders][8]
    *   [Creating a Program Object and Linking the Shaders][9]
    *   [Setting the Viewport and Clearing the Color Buffer][10]
    *   [Loading the Geometry and Drawing a Primitive][11]
    *   [Displaying the Back Buffer][12]
*   [An Introduction to EGL][13] 
    *   [Communicating with the Windowing System][14]
    *   [Checking for Errors][15]
    *   [Initializing EGL][16]
    *   [Determining the Available Surface Configurations][17]
    *   [Querying EGLConfig Attributes][18]
    *   [Letting EGL Choose the Configuration][19]
    *   [Creating an On-Screen Rendering Area: The EGL Window][20]
    *   [Creating an Off-Screen Rendering Area: EGL Pbuffers][21]
    *   [Creating a Rendering Context][22]
    *   [Making an EGLContext Current][23]
    *   [Putting All Our EGL Knowledge Together][24]
    *   [Synchronizing Rendering][25]
*   [Shaders and Programs][26] 
    *   [Shaders and Programs][27] 
        *   [Creating and Compiling a Shader][28]
        *   [Creating and Linking a Program][29]
    *   [Uniform and Attributes][30] 
        *   [Getting and Setting Uniforms][31]
        *   [Uniform Buffer Objects][32]
        *   [Getting and Setting Attributes]
    *   [Shader Compiler]
    *   [Program Binaries]
    *   [Summary]
*   [OpenGL ES Shading Language] 
    *   [OpenGL ES Shading Language Basics]
    *   [Shader Version Specification]
    *   [Variables and Variable Types]
    *   [Variable Constructors]
    *   [Vector and Matrix Components]
    *   [Constants]
    *   [Structures]
    *   [Arrays]
    *   [Operators]
    *   [Functions]
    *   [Built-In Functions]
    *   [Control Flow Statements]
    *   [Uniforms]
    *   [Uniform Blocks]
    *   [Vertex and Fragment Shader Inputs/Outputs]
    *   [Interpolation Qualifiers]
    *   [Preprocessor and Directives]
    *   [Uniform and Interpolator Packing]
    *   [Precision Qualifiers]
    *   [Invariance]
    *   [Summary]
*   （未完）

 [1]: http://blog.copper3d.org/OpenGL_ES_3.0/introduction_to_opengl_es_30/README.html
 [2]: http://blog.copper3d.org/OpenGL_ES_3.0/hello_triangle_an_opengl_es_30_example/README.html
 [3]: http://blog.copper3d.org/OpenGL_ES_3.0/hello_triangle_an_opengl_es_30_example/code_framework.html
 [4]: http://blog.copper3d.org/OpenGL_ES_3.0/hello_triangle_an_opengl_es_30_example/where_to_download_the_examples.html
 [5]: http://blog.copper3d.org/OpenGL_ES_3.0/hello_triangle_an_opengl_es_30_example/hello_triangle_example.html
 [6]: http://blog.copper3d.org/OpenGL_ES_3.0/hello_triangle_an_opengl_es_30_example/using_the_opengl_es_30_framework.html
 [7]: http://blog.copper3d.org/OpenGL_ES_3.0/hello_triangle_an_opengl_es_30_example/creating_a_simple_vertex_and_fragment_shader.html
 [8]: http://blog.copper3d.org/OpenGL_ES_3.0/hello_triangle_an_opengl_es_30_example/compiling_and_loading_the_shaders.html
 [9]: http://blog.copper3d.org/OpenGL_ES_3.0/hello_triangle_an_opengl_es_30_example/creating_a_program_object_and_linking_the_shaders.html
 [10]: http://blog.copper3d.org/OpenGL_ES_3.0/hello_triangle_an_opengl_es_30_example/setting_the_viewport_and_clearing_the_color_buffer.html
 [11]: http://blog.copper3d.org/OpenGL_ES_3.0/hello_triangle_an_opengl_es_30_example/loading_the_geometry_and_drawing_a_primitive.html
 [12]: http://blog.copper3d.org/OpenGL_ES_3.0/hello_triangle_an_opengl_es_30_example/displaying_the_back_buffer.html
 [13]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/README.html
 [14]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/communicating_with_the_windowing_system.html
 [15]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/checking_for_errors.html
 [16]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/initializing_egl.html
 [17]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/determining_the_available_surface_configurations.html
 [18]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/querying_eglconfig_attributes.html
 [19]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/letting_egl_choose_the_configuration.html
 [20]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/creating_an_on-screen_rendering_area_the_egl_window.html
 [21]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/creating_an_off-screen_rendering_area_egl_pbuffers.html
 [22]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/creating_a_rendering_context.html
 [23]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/making_an_eglcontext_current.html
 [24]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/putting_all_our_egl_knowledge_together.html
 [25]: http://blog.copper3d.org/OpenGL_ES_3.0/an_introduction_to_egl/synchronizing_rendering.html
 [26]: http://blog.copper3d.org/OpenGL_ES_3.0/shaders_and_programs/README.html
 [27]: http://blog.copper3d.org/OpenGL_ES_3.0/shaders_and_programs/shader_and_programs.html
 [28]: http://blog.copper3d.org/OpenGL_ES_3.0/shaders_and_programs/qq.html
 [29]: http://blog.copper3d.org/OpenGL_ES_3.0/shaders_and_programs/creating_and_linking_a_program.html
 [30]: http://blog.copper3d.org/OpenGL_ES_3.0/shaders_and_programs/uniform_and_attributes.html
 [31]: http://blog.copper3d.org/OpenGL_ES_3.0/shaders_and_programs/getting_and_setting_uniforms.html
 [32]: http://blog.copper3d.org/OpenGL_ES_3.0/shaders_and_programs/uniform_buffer_objects.html