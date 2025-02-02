#include "raylib.h"
#include <cstring>
#define MAX_INPUT_CHARS 12
using namespace std;

// عرض و ارتفاع صفحه بازی
const int width = 700;
const int height = 400;

int main()
{
    InitWindow(width , height , "TicTacToe");
    bool close_window = true;
    bool human = false , restart = false , exit = false , user = false , theme = false , question = false , user_tmp = false;
    int frame = 0;

    struct 
    {
        //---------------------------
        //    برای حالت بازی انسانی 
        //            |
        //            |
        //            |
        //           \ /
        //            V
        //--------------------------
        char a[3][3] = {{'0' , '0' , '0'} , {'0' , '0' , '0'} , {'0' , '0' , '0'}};
        bool b[3][3] = {{0 , 0 , 0} , {0 , 0 , 0} , {0 , 0 , 0}};
        bool player1 = true;
        bool player2 = false;
        bool player1_win = false;
        bool player2_win = false;
        int player1_win_counter = 0; 
        int player2_win_counter = 0; 
        int draw_counter = 0;
        bool draw = false;
        int turn = 0;
        bool player1_name_is_changed = false;
        bool player2_name_is_changed = false;
        //---------------------------
        //برای تغییر نام بازیکن
        //              |
        //              |
        //              |
        //             \ /
        //              V
        //--------------------------
        char player1_name[25] = "\0";
        char player2_name[25] = "\0";
        int player1_letter_count = 0; 
        int player2_letter_count = 0;
    } game ;


    // بارگذاری تصاویر در بازی
    Image image_ico = LoadImage("setting.jpg");     
    Texture2D texture = LoadTextureFromImage(image_ico);         
    UnloadImage(image_ico); 
    Image user_ico = LoadImage("user.jpg");     
    Texture2D texture1 = LoadTextureFromImage(user_ico);         
    UnloadImage(user_ico);
    Image theme_ico = LoadImage("theme.jpg");     
    Texture2D texture2 = LoadTextureFromImage(theme_ico);         
    UnloadImage(theme_ico);
    Image question_ico = LoadImage("question.jpg");     
    Texture2D texture3 = LoadTextureFromImage(question_ico);         
    UnloadImage(question_ico);
    Image exit_ico = LoadImage("exit.jpg");     
    Texture2D texture4 = LoadTextureFromImage(exit_ico);         
    UnloadImage(exit_ico);
    Image restart_ico = LoadImage("restart.jpg");     
    Texture2D texture5 = LoadTextureFromImage(restart_ico);         
    UnloadImage(restart_ico);

    // بارگذاری صداها در بازی
    InitAudioDevice();
    Sound button = LoadSound("button.mp3");
    Sound win = LoadSound("win.wav");
    Sound placing = LoadSound("placing.mp3");

    SetTargetFPS(60);

    while(!WindowShouldClose() && close_window)
    {

    // موقعیت ماوس
    struct 
    {
        float x = GetMouseX();
        float y = GetMouseY();
    } mouse ;
     
        BeginDrawing();
        ClearBackground(BLACK);

        // انتظار برای دور بعدی
        if (human)
        {
            if (frame >= 150)
            {
                frame = 0;
                game.turn = 0;
                if ((game.player1_win_counter + game.player2_win_counter + game.draw_counter) % 2 == 0)
                {
                    game.player1 = true;
                    game.player2 = false;
                }
                else 
                {
                    game.player1 = false;
                    game.player2 = true;
                }
                game.player1_win = false;
                game.player2_win = false;
                game.draw = false;
                for (int i = 0 ; i<3 ; i++)
                {
                    for (int j = 0 ; j<3 ; j++)
                    {
                        game.a[i][j] = '0';
                    }
                }
                for (int i = 0 ; i<3 ; i++)
                {
                    for (int j = 0 ; j<3 ; j++)
                    {
                        game.b[i][j] = 0;
                    }
                }
            }
        }

        // بازنشانی
        if (human)
        {
            DrawTexture(texture5, 5 , 305 , WHITE);
        }

        if (restart)
        {
            frame = 0;
            game.turn = 0;
            game.player1 = true;
            game.player2 = false;
            game.player1_win = false;
            game.player2_win = false;
            game.draw = false;
            game.player1_win_counter = 0;
            game.player2_win_counter = 0;
            game.draw_counter = 0;
            for (int i = 0 ; i<3 ; i++)
            {
                for (int j = 0 ; j<3 ; j++)
                {
                    game.a[i][j] = '0';
                }
            }
            for (int i = 0 ; i<3 ; i++)
            {
                for (int j = 0 ; j<3 ; j++)
                {
                    game.b[i][j] = 0;
                }
            }
            restart = false;
        }

        // خروج
        if (human || user || theme || question)
        {
            DrawTexture(texture4, -5 , 345 , WHITE);
        }

        // سوال
        if (!human && !user && !theme && !question)
        {
            DrawTexture(texture3, 0 , 300 , WHITE);
        }
        if (question)
        {
            DrawText("How to Play" , 0 , 0 , 40 , WHITE );
            DrawText("1. the game is played on a grid that's 3 squares by 3 squares" , 0 , 50 , 20 , WHITE );
            DrawText("2. you are O and your friend (or the robot in this case) is X" , 0 , 80 , 20 , WHITE );
            DrawText("3. players take turns putting their marks in empty squares" , 0 , 110 , 20 , WHITE );
            DrawText("4. the first player to get 3 of her marks in a row (up, down, across" , 0 , 140 , 20 , WHITE );
            DrawText("or diagonally) is the winner" , 0 , 170 , 20 , WHITE );
            DrawText("5. when all 9 squares are full, the game is over" , 0 , 200 , 20 , WHITE );
            DrawText("6. if no player has 3 marks in a row, the game ends in a draw" , 0 , 230 , 20 , WHITE );
        }

        // رسم دایره‌های سبز و قرمز برای اجازه دادن به بازیکن برای بازی
        if ((!game.player1_name_is_changed || !game.player2_name_is_changed) && (!user && !theme && !question))
        {
            DrawCircle(420 , 172 , 10 , RED);
            DrawCircle(60 , 375 , 10 , GREEN);
        }
        if (game.player1_name_is_changed && game.player2_name_is_changed && !human && !user && !theme && !question)
        {
            DrawCircle(420 , 172 , 10 , GREEN);
        }

        // کاربر
        if (!human && !user && !theme && !question)
        {
            DrawTexture(texture1, 0 , 350 , WHITE);
        }
        
        if (user)
        {
            DrawText("Player1 : " , 10 , 20 , 30 , BLUE);
            DrawText("Player2 : " , 10 , 70 , 30 , RED);
            DrawRectangle(160 , 20 , 400  , 30 , WHITE);
            DrawRectangle(160 , 70 , 400  , 30 , WHITE);
            DrawText("1. names must not be same" , 10 , 120 , 20 , WHITE);
            DrawText("2. you should use at least 1 character and at last 12 character" , 10 , 160 , 20 , WHITE);
            if (mouse.x>=160 && mouse.x<=560 && mouse.y>=20 && mouse.y<=50)   
            {
                SetMouseCursor(MOUSE_CURSOR_IBEAM); 
                int key = GetCharPressed();


                while (key > 0)
                {
                    if ((key >= 32) && (key <= 125) && (game.player1_letter_count < MAX_INPUT_CHARS))
                    {
                        game.player1_name[game.player1_letter_count] = (char)key;
                        game.player1_name[game.player1_letter_count+1] = '\0';
                        game.player1_letter_count++;
                    }

                    key = GetCharPressed();  
                }

                if (IsKeyPressed(KEY_BACKSPACE))
                {
                    game.player1_letter_count--;
                    if (game.player1_letter_count < 0) game.player1_letter_count = 0;
                    game.player1_name[game.player1_letter_count] = '\0';
                }

            }
            else if (mouse.x>=160 && mouse.x<=560 && mouse.y>=70 && mouse.y<=100)   
            {
                SetMouseCursor(MOUSE_CURSOR_IBEAM);
                int key = GetCharPressed();


                while (key > 0)
                {
                    if ((key >= 32) && (key <= 125) && (game.player2_letter_count < MAX_INPUT_CHARS))
                    {
                        game.player2_name[game.player2_letter_count] = (char)key;
                        game.player2_name[game.player2_letter_count+1] = '\0';
                        game.player2_letter_count++;
                    }

                    key = GetCharPressed();  
                }

                if (IsKeyPressed(KEY_BACKSPACE))
                {
                    game.player2_letter_count--;
                    if (game.player2_letter_count < 0) game.player2_letter_count = 0;
                    game.player2_name[game.player2_letter_count] = '\0';
                }
            } 
            else
            {
                SetMouseCursor(MOUSE_CURSOR_DEFAULT);
            }

            if (strcmp(game.player1_name , game.player2_name) != 0)
            {
                if (game.player1_letter_count == 0)
                {
                    DrawCircle( 580 , 35 , 10 , RED);
                    game.player1_name_is_changed = false;
                }
                else
                {
                    DrawCircle( 580 , 35 , 10 , GREEN);
                    game.player1_name_is_changed = true;
                }
                
                if (game.player2_letter_count == 0)
                {
                    DrawCircle( 580 , 85 , 10 , RED);
                    game.player2_name_is_changed = false;
                }
                else
                {
                    DrawCircle( 580 , 85 , 10 , GREEN);
                    game.player2_name_is_changed = true;
                }
            }
            else
            {
                DrawCircle( 580 , 85 , 10 , RED);
                DrawCircle( 580 , 35 , 10 , RED);
                game.player1_name_is_changed = false;
                game.player2_name_is_changed = false;
            }

            DrawText(game.player1_name, 165 , 20 , 30, BLUE);
            DrawText(game.player2_name, 165 , 70 , 30, RED);
        }

        // متن در وسط (تیک تک تو، انسانی، خروج)
        if (!human && !user && !theme && !question)
        {
            DrawText("TicTacToe" , width/2 - 165 , 5 , 60 , WHITE);
        }
        if (!human && !user && !theme && !question)
        {
            DrawText("Play" , width/2 - 35 , 150 , 40 , WHITE);
        }
        if (!human && !user && !theme && !question)
        {
            DrawText("Exit" , width/2 - 30 , 300 , 40 , WHITE);
        }

        // در حالت انسانی برای امتیاز
        if (human)
        {
            if (game.player1)
            {
                DrawText("Turn(O) : " , 0 , 5 , 20 , WHITE);
                DrawText(game.player1_name , 100 , 5 , 20 , BLUE);
            }
            else if (game.player2)
            {
                DrawText("Turn(X) : " , 0 , 5 , 20 , WHITE);
                DrawText(game.player2_name , 100 , 5 , 20 , RED);
            }

            DrawText(TextFormat( game.player1_name) , 0 , 30 , 20 , BLUE);
            DrawText( ":" , MeasureText(game.player1_name , 20) + 10 , 30 , 20 , BLUE);
            DrawText(TextFormat("%i" , game.player1_win_counter) , MeasureText(game.player1_name , 20) + 20 , 30 , 20 , BLUE);

            DrawText(TextFormat( game.player2_name) , 0 , 60 , 20 , RED);
            DrawText( ":" , MeasureText(game.player2_name , 20) + 10 , 60 , 20 , RED);
            DrawText(TextFormat("%i" , game.player2_win_counter) , MeasureText(game.player2_name , 20) + 20 , 60 , 20 , RED);
            
            DrawText("Draw" , 0 , 90 , 20 , WHITE);
            DrawText( ":" , MeasureText("Draw" , 20) + 10 , 90 , 20 , WHITE);
            DrawText(TextFormat("%i" , game.draw_counter) , MeasureText("Draw" , 20) + 20 , 90 , 20 , WHITE);
        }
        if ((game.draw || game.player1_win || game.player2_win) && (human))
        {
            if (game.draw)
            {
                DrawText("Draw!" , 80 , 150 , 40 , WHITE); 
            }
            else if (game.player1_win)
            {
                DrawText( game.player1_name , 15 , 150 , 30 , BLUE);
                DrawText( "Won!" , 15 + 8 + MeasureText(game.player1_name , 30) , 150 , 30 , BLUE);
            }
            else if (game.player2_win)
            {
                DrawText( game.player2_name , 15 , 150 , 30 , RED);
                DrawText( "Won!" , 15 + 8 + MeasureText(game.player2_name , 30) , 150 , 30 , RED);
            }

        }


        // طراحی بازی برای حالت انسانی
        if (human)
        {
            DrawLineEx({700 - 410 , 140} , {700 - 20 , 140} , 15 , WHITE);
            DrawLineEx({700 - 410 , 260} , {700 - 20 , 260} , 15 , WHITE); 

            DrawLineEx({700 - 290 , 20} , {700 - 290 , 400 - 20} , 15 , WHITE);
            DrawLineEx({700 - 155 , 20} , {700 - 155 , 400 - 20} , 15 , WHITE);  

            // a[0][0]
            if (game.a[0][0] == '0' && mouse.x >= 700 - 410 && mouse.x <= 700 - 410 + 120 && mouse.y >= 20 && mouse.y<=140 && !(game.draw || game.player1_win || game.player2_win))
            {
                if (game.player1)
                {
                    DrawRing({290 + 120/2 - 5 , 20 + 120/2 - 5} , 40  , 50  , 0 , 360 , 3 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[0][0] = 'O';
                        game.player1 = false;
                        game.player2 = true;
                        PlaySound(placing);
                    }
                }
                else if (game.player2)
                {
                    DrawLineEx({290 + 15 , 20 + 5 } , {290 + 120 - 25 , 120 - 5} , 10 , GRAY);
                    DrawLineEx({290 + 120 - 25 , 20 + 5 } , {290 + 15 , 120 - 5} , 10 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[0][0] = 'X';
                        game.player1 = true;
                        game.player2 = false;
                        PlaySound(placing);
                    }
                }
            }

            if (game.a[0][0] == 'O' && !game.b[0][0])
            {
                DrawRing({290 + 120/2 - 5 , 20 + 120/2 - 5} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            else if (game.a[0][0] == 'O' && game.b[0][0])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                DrawRing({290 + 120/2 - 5 , 20 + 120/2 - 5} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            
            if (game.a[0][0] == 'X' && !game.b[0][0])
            {
                DrawLineEx({290 + 15 , 20 + 5 } , {290 + 120 - 25 , 120 - 5} , 10 , RED);
                DrawLineEx({290 + 120 - 25 , 20 + 5 } , {290 + 15 , 120 - 5} , 10 , RED);
            }
            else if (game.a[0][0] == 'X' && game.b[0][0])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                {
                   DrawLineEx({290 + 15 , 20 + 5 } , {290 + 120 - 25 , 120 - 5} , 10 , RED);
                    DrawLineEx({290 + 120 - 25 , 20 + 5 } , {290 + 15 , 120 - 5} , 10 , RED); 
                }
                
            }
            

            // a[0][1]
            if (game.a[0][1] == '0' && mouse.x >= 700 - 410 + 145 && mouse.x <= 700 - 410 + 120 + 145 && mouse.y >= 20 && mouse.y<=140 && !(game.draw || game.player1_win || game.player2_win))
            {
                if (game.player1)
                {
                    DrawRing({290 + 135 + 120/2 - 5 , 20 + 120/2 - 5} , 40  , 50  , 0 , 360 , 3 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[0][1] = 'O';
                        game.player1 = false;
                        game.player2 = true;
                        PlaySound(placing);
                    }
                }
                else if (game.player2)
                {
                    DrawLineEx({290 + 15 + 135 , 20 + 5 } , {290 + 120 - 25 + 135, 120 - 5} , 10 , GRAY);
                    DrawLineEx({290 + 120 - 25 + 135 , 20 + 5 } , {290 + 15 + 135, 120 - 5} , 10 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[0][1] = 'X';
                        game.player1 = true;
                        game.player2 = false;
                        PlaySound(placing);
                    }
                }
            }

            if (game.a[0][1] == 'O' && !game.b[0][1])
            {
                DrawRing({290 + 135 + 120/2 - 5 , 20 + 120/2 - 5} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            else if (game.a[0][1] == 'O' && game.b[0][1])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                DrawRing({290 + 135 + 120/2 - 5 , 20 + 120/2 - 5} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            if (game.a[0][1] == 'X' && !game.b[0][1])
            {
                DrawLineEx({290 + 15 + 135, 20 + 5 } , {290 + 120 - 25 + 135, 120 - 5} , 10 , RED);
                DrawLineEx({290 + 120 - 25 + 135, 20 + 5 } , {290 + 15 + 135, 120 - 5} , 10 , RED);
            }
            else if (game.a[0][1] == 'X' && game.b[0][1])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                {
                    DrawLineEx({290 + 15 + 135, 20 + 5 } , {290 + 120 - 25 + 135, 120 - 5} , 10 , RED);
                    DrawLineEx({290 + 120 - 25 + 135, 20 + 5 } , {290 + 15 + 135, 120 - 5} , 10 , RED);
                }
            }

            // a[0][2]
            if (game.a[0][2] == '0' && mouse.x >= 700 - 410 + 145 + 145 && mouse.x <= 700 - 410 + 120 + 145 + 145 && mouse.y >= 20 && mouse.y<=140 && !(game.draw || game.player1_win || game.player2_win))
            {
                if (game.player1)
                {
                    DrawRing({290 + 135 + 135 + 120/2 - 5 , 20 + 120/2 - 5} , 40  , 50  , 0 , 360 , 3 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[0][2] = 'O';
                        game.player1 = false;
                        game.player2 = true;
                        PlaySound(placing);
                    }
                }
                else if (game.player2)
                {
                    DrawLineEx({290 + 15 + 135 + 135 , 20 + 5 } , {290 + 120 - 25 + 135 + 135, 120 - 5} , 10 , GRAY);
                    DrawLineEx({290 + 120 - 25 + 135 + 135 , 20 + 5 } , {290 + 15 + 135 + 135, 120 - 5} , 10 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[0][2] = 'X';
                        game.player1 = true;
                        game.player2 = false;
                        PlaySound(placing);
                    }
                }
            }

            if (game.a[0][2] == 'O' && !game.b[0][2])
            {
                DrawRing({290 + 135 + 135 + 120/2 - 5 , 20 + 120/2 - 5} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            else if (game.a[0][2] == 'O' && game.b[0][2])
            {
                //(frame>=0 && frame<=15) || (frame>=30 && frame<=45) || (frame>=60 && frame<=75) // initial
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                DrawRing({290 + 135 + 135 + 120/2 - 5 , 20 + 120/2 - 5} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            if (game.a[0][2] == 'X' && !game.b[0][2])
            {
                DrawLineEx({290 + 15 + 135 + 135 , 20 + 5 } , {290 + 120 - 25 + 135 + 135 , 120 - 5} , 10 , RED);
                DrawLineEx({290 + 120 - 25 + 135 + 135 , 20 + 5 } , {290 + 15 + 135 + 135 , 120 - 5} , 10 , RED);
            }
            else if (game.a[0][2] == 'X' && game.b[0][2])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                {
                    DrawLineEx({290 + 15 + 135 + 135 , 20 + 5 } , {290 + 120 - 25 + 135 + 135 , 120 - 5} , 10 , RED);
                    DrawLineEx({290 + 120 - 25 + 135 + 135 , 20 + 5 } , {290 + 15 + 135 + 135 , 120 - 5} , 10 , RED);
                }
            }

            // a[1][0]
            if (game.a[1][0] == '0' && mouse.x >= 700 - 410 && mouse.x <= 700 - 410 + 135 && mouse.y >= 20 + 120 && mouse.y<=140 + 135 && !(game.draw || game.player1_win || game.player2_win))
            {
                if (game.player1)
                {
                    DrawRing({290 + 120/2 - 5 , 20 + 120/2 + 135 - 15} , 40  , 50  , 0 , 360 , 3 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[1][0] = 'O';
                        game.player1 = false;
                        game.player2 = true;
                        PlaySound(placing);
                    }
                }
                else if (game.player2)
                {
                    DrawLineEx({290 + 15 , 20 + 5 + 135 - 5} , {290 + 120 - 25 , 120 - 10 + 135} , 10 , GRAY);
                    DrawLineEx({290 + 120 - 25 , 20 + 5 + 135 - 5 } , {290 + 15 , 120 - 10 + 135} , 10 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[1][0] = 'X';
                        game.player1 = true;
                        game.player2 = false;
                        PlaySound(placing);
                    }
                }
            }

            if (game.a[1][0] == 'O' && !game.b[1][0])
            {
                DrawRing({290 + 120/2 - 5 , 20 + 135 + 120/2 - 15} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            else if (game.a[1][0] == 'O' && game.b[1][0])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                DrawRing({290 + 120/2 - 5 , 20 + 135 + 120/2 - 15} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            if (game.a[1][0] == 'X' && !game.b[1][0])
            {
                DrawLineEx({290 + 15 , 20 + 5 + 135 - 5} , {290 + 120 - 25 , 120 - 10 + 135} , 10 , RED);
                DrawLineEx({290 + 120 - 25 , 20 + 5 + 135 - 5 } , {290 + 15 , 120 - 10 + 135} , 10 , RED);
            }
            else if (game.a[1][0] == 'X' && game.b[1][0])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                {
                    DrawLineEx({290 + 15 , 20 + 5 + 135 - 5} , {290 + 120 - 25 , 120 - 10 + 135} , 10 , RED);
                    DrawLineEx({290 + 120 - 25 , 20 + 5 + 135 - 5 } , {290 + 15 , 120 - 10 + 135} , 10 , RED);
                }
            }

            // a[1][1]
            if (game.a[1][1] == '0' && mouse.x >= 700 - 410 + 145 && mouse.x <= 700 - 410 + 120 + 145 && mouse.y >= 20 + 135 && mouse.y<=140 + 135 && !(game.draw || game.player1_win || game.player2_win))
            {
                if (game.player1)
                {
                    DrawRing({290 + 135 + 120/2 - 5 , 20 + 135 + 120/2 - 15} , 40  , 50  , 0 , 360 , 3 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[1][1] = 'O';
                        game.player1 = false;
                        game.player2 = true;
                        PlaySound(placing);
                    }
                }
                else if (game.player2)
                {
                    DrawLineEx({290 + 15 + 135 , 20 + 5 + 135  - 5} , {290 + 120 - 25 + 135, 120 - 10 + 135} , 10 , GRAY);
                    DrawLineEx({290 + 120 - 25 + 135 , 20 + 5 + 135 - 5 } , {290 + 15 + 135, 120 - 10 + 135 } , 10 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[1][1] = 'X';
                        game.player1 = true;
                        game.player2 = false;
                        PlaySound(placing);
                    }
                }
            }

            if (game.a[1][1] == 'O' && !game.b[1][1])
            {
                DrawRing({290 + 135 + 120/2 - 5 , 20 + 120/2 - 15 + 135} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            else if (game.a[1][1] == 'O' && game.b[1][1])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                DrawRing({290 + 135 + 120/2 - 5 , 20 + 120/2 - 15 + 135} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            if (game.a[1][1] == 'X' && !game.b[1][1])
            {
                DrawLineEx({290 + 15 + 135, 20 + 5 + 135 - 5} , {290 + 120 - 25 + 135, 120 - 10 + 135 } , 10 , RED);
                DrawLineEx({290 + 120 - 25 + 135, 20 + 5 + 135 - 5} , {290 + 15 + 135, 120 - 10 + 135 } , 10 , RED);
            }
            else if (game.a[1][1] == 'X' && game.b[1][1])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                {
                    DrawLineEx({290 + 15 + 135, 20 + 5 + 135 - 5} , {290 + 120 - 25 + 135, 120 - 10 + 135 } , 10 , RED);
                    DrawLineEx({290 + 120 - 25 + 135, 20 + 5 + 135 - 5} , {290 + 15 + 135, 120 - 10 + 135 } , 10 , RED);
                }
            }
            // a[1][2]
            if (game.a[1][2] == '0' && mouse.x >= 700 - 410 + 145 + 145 && mouse.x <= 700 - 410 + 120 + 145 + 145 && mouse.y >= 20 + 120 && mouse.y<=140 + 120 && !(game.draw || game.player1_win || game.player2_win))
            {
                if (game.player1)
                {
                    DrawRing({290 + 135 + 135 + 120/2 - 5 , 20 + 135 + 120/2 - 15} , 40  , 50  , 0 , 360 , 3 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[1][2] = 'O';
                        game.player1 = false;
                        game.player2 = true;
                        PlaySound(placing);
                    }
                }
                else if (game.player2)
                {
                    DrawLineEx({290 + 15 + 135 + 135 , 20 + 135 } , {290 + 120 - 25 + 135 + 135, 120 - 5 + 135 - 10} , 10 , GRAY);
                    DrawLineEx({290 + 120 - 25 + 135 + 135 , 20 + 135 } , {290 + 15 + 135 + 135, 120 - 5 + 135 - 10} , 10 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[1][2] = 'X';
                        game.player1 = true;
                        game.player2 = false;
                        PlaySound(placing);
                    }
                }
            }

            if (game.a[1][2] == 'O' && !game.b[1][2])
            {
                DrawRing({290 + 135 + 135 + 120/2 - 5 , 20 + 120/2 + 135 - 15} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            else if (game.a[1][2] == 'O' && game.b[1][2])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                DrawRing({290 + 135 + 135 + 120/2 - 5 , 20 + 120/2 + 135 - 15} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            if (game.a[1][2] == 'X' && !game.b[1][2])
            {
                DrawLineEx({290 + 15 + 135 + 135 , 20 + 5 + 135 - 5 } , {290 + 120 - 25 + 135 + 135 , 120 - 5 - 10 + 135} , 10 , RED);
                DrawLineEx({290 + 120 - 25 + 135 + 135 , 20 + 5 + 135 - 5 } , {290 + 15 + 135 + 135 , 120 - 5 - 10 + 135} , 10 , RED);
            }
            else if (game.a[1][2] == 'X' && game.b[1][2])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                {
                    DrawLineEx({290 + 15 + 135 + 135 , 20 + 5 + 135 - 5 } , {290 + 120 - 25 + 135 + 135 , 120 - 5 - 10 + 135} , 10 , RED);
                    DrawLineEx({290 + 120 - 25 + 135 + 135 , 20 + 5 + 135 - 5 } , {290 + 15 + 135 + 135 , 120 - 5 - 10 + 135} , 10 , RED);
                }
            }

            // a[2][0]
            if (game.a[2][0] == '0' && mouse.x >= 700 - 410 && mouse.x <= 700 - 410 + 135 && mouse.y >= 20 + 2*135 && mouse.y<=140 + 2*135 && !(game.draw || game.player1_win || game.player2_win))
            {
                if (game.player1)
                {
                    DrawRing({290 + 120/2 - 5 , 20 + 120/2 + 2*135 - 15 - 10} , 40  , 50  , 0 , 360 , 3 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[2][0] = 'O';
                        game.player1 = false;
                        game.player2 = true;
                        PlaySound(placing);
                    }
                }
                else if (game.player2)
                {
                    DrawLineEx({290 + 15 , 20 + 5 + 2*135 - 5 - 5} , {290 + 120 - 25 , 120 - 10 + 2*135 - 5} , 10 , GRAY);
                    DrawLineEx({290 + 120 - 25 , 20 + 5 + 2*135 - 5 - 5 } , {290 + 15 , 120 - 10 + 2*135 - 5} , 10 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[2][0] = 'X';
                        game.player1 = true;
                        game.player2 = false;
                        PlaySound(placing);
                    }
                }
            }

            if (game.a[2][0] == 'O' && !game.b[2][0])
            {
                DrawRing({290 + 120/2 - 5 , 20 + 2*135 + 120/2 - 15 - 10} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            else if (game.a[2][0] == 'O' && game.b[2][0])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                DrawRing({290 + 120/2 - 5 , 20 + 2*135 + 120/2 - 15 - 10} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            if (game.a[2][0] == 'X' && !game.b[2][0])
            {
                DrawLineEx({290 + 15 , 20 + 5 + 2*135 - 5 - 5} , {290 + 120 - 25 , 120 - 10 + 2*135 - 5} , 10 , RED);
                DrawLineEx({290 + 120 - 25 , 20 + 5 + 2*135 - 5 - 5} , {290 + 15 , 120 - 10 + 2*135 - 5} , 10 , RED);
            }
            else if (game.a[2][0] == 'X' && game.b[2][0])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                {
                    DrawLineEx({290 + 15 , 20 + 5 + 2*135 - 5 - 5} , {290 + 120 - 25 , 120 - 10 + 2*135 - 5} , 10 , RED);
                    DrawLineEx({290 + 120 - 25 , 20 + 5 + 2*135 - 5 - 5} , {290 + 15 , 120 - 10 + 2*135 - 5} , 10 , RED);
                }
            }

            // a[2][1]
            if (game.a[2][1] == '0' && mouse.x >= 700 - 410 + 145 && mouse.x <= 700 - 410 + 120 + 145 && mouse.y >= 20 + 2*135 && mouse.y<=140 + 2*135 && !(game.draw || game.player1_win || game.player2_win))
            {
                if (game.player1)
                {
                    DrawRing({290 + 135 + 120/2 - 5 , 20 + 2*135 + 120/2 - 25} , 40  , 50  , 0 , 360 , 3 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[2][1] = 'O';
                        game.player1 = false;
                        game.player2 = true;
                        PlaySound(placing);
                    }
                }
                else if (game.player2)
                {
                    DrawLineEx({290 + 15 + 135 , 20 + 5 + 2*135  - 5 - 5} , {290 + 120 - 25 + 135, 120 - 10 + 2*135 - 5} , 10 , GRAY);
                    DrawLineEx({290 + 120 - 25 + 135 , 20 + 5 + 2*135 - 5 - 5} , {290 + 15 + 135, 120 - 10 + 2*135 - 5 } , 10 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[2][1] = 'X';
                        game.player1 = true;
                        game.player2 = false;
                        PlaySound(placing);
                    }
                }
            }

            if (game.a[2][1] == 'O' && !game.b[2][1])
            {
                DrawRing({290 + 135 + 120/2 - 5 , 20 + 120/2 - 15 + 2*135 - 10} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            else if (game.a[2][1] == 'O' && game.b[2][1])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                DrawRing({290 + 135 + 120/2 - 5 , 20 + 120/2 - 15 + 2*135 - 10} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            if (game.a[2][1] == 'X' && !game.b[2][1])
            {
                DrawLineEx({290 + 15 + 135, 20 + 5 + 2*135 - 5 - 5} , {290 + 120 - 25 + 135, 120 - 10 + 2*135 - 5 } , 10 , RED);
                DrawLineEx({290 + 120 - 25 + 135, 20 + 5 + 2*135 - 5 - 5} , {290 + 15 + 135, 120 - 10 + 2*135 - 5 } , 10 , RED);
            }
            else if (game.a[2][1] == 'X' && game.b[2][1])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                {
                    DrawLineEx({290 + 15 + 135, 20 + 5 + 2*135 - 5 - 5} , {290 + 120 - 25 + 135, 120 - 10 + 2*135 - 5 } , 10 , RED);
                    DrawLineEx({290 + 120 - 25 + 135, 20 + 5 + 2*135 - 5 - 5} , {290 + 15 + 135, 120 - 10 + 2*135 - 5 } , 10 , RED);
                }
            }

            // a[2][2]
            if (game.a[2][2] == '0' && mouse.x >= 700 - 410 + 145 + 145 && mouse.x <= 700 - 410 + 120 + 145 + 145 && mouse.y >= 20 + 2*135 && mouse.y<=140 + 2*135 && !(game.draw || game.player1_win || game.player2_win))
            {
                if (game.player1)
                {
                    DrawRing({290 + 135 + 135 + 120/2 - 5 , 20 + 2*135 + 120/2 - 25} , 40  , 50  , 0 , 360 , 3 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[2][2] = 'O';
                        game.player1 = false;
                        game.player2 = true;
                        PlaySound(placing);
                    }
                }
                else if (game.player2)
                {
                    DrawLineEx({290 + 15 + 135 + 135 , 20 + 2*135 - 5 } , {290 + 120 - 25 + 135 + 135, 120 - 5 + 2*135 - 10 - 5} , 10 , GRAY);
                    DrawLineEx({290 + 120 - 25 + 135 + 135 , 20 + 2*135 - 5 } , {290 + 15 + 135 + 135, 120 - 5 + 2*135 - 10 - 5} , 10 , GRAY);
                    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
                    {
                        game.turn++;
                        game.a[2][2] = 'X';
                        game.player1 = true;
                        game.player2 = false;
                        PlaySound(placing);
                    }
                }
            }

            if (game.a[2][2] == 'O' && !game.b[2][2])
            {
                DrawRing({290 + 135 + 135 + 120/2 - 5 , 20 + 120/2 + 2*135 - 25} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            else if (game.a[2][2] == 'O' && game.b[2][2])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                DrawRing({290 + 135 + 135 + 120/2 - 5 , 20 + 120/2 + 2*135 - 25} , 40  , 50  , 0 , 360 , 3 , BLUE);
            }
            if (game.a[2][2] == 'X' && !game.b[2][2])
            {
                DrawLineEx({290 + 15 + 135 + 135 , 20 + 5 + 2*135 - 5  - 5} , {290 + 120 - 25 + 135 + 135 , 120 - 5 - 10 + 2*135 - 5} , 10 , RED);
                DrawLineEx({290 + 120 - 25 + 135 + 135 , 20 + 5 + 2*135 - 5  - 5} , {290 + 15 + 135 + 135 , 120 - 5 - 10 + 2*135 - 5} , 10 , RED);
            }
            else if (game.a[2][2] == 'X' && game.b[2][2])
            {
                if ((frame>=0 && frame<=30) || (frame>=60 && frame<=90) || (frame>=120 && frame<=150))
                {
                    DrawLineEx({290 + 15 + 135 + 135 , 20 + 5 + 2*135 - 5  - 5} , {290 + 120 - 25 + 135 + 135 , 120 - 5 - 10 + 2*135 - 5} , 10 , RED);
                    DrawLineEx({290 + 120 - 25 + 135 + 135 , 20 + 5 + 2*135 - 5  - 5} , {290 + 15 + 135 + 135 , 120 - 5 - 10 + 2*135 - 5} , 10 , RED);
                }
            }
        }

        // قوانین بازی برای حالت انسانی

        if ((game.a[0][0] == 'O' && game.a[1][1] == 'O' && game.a[2][2] == 'O') || (game.a[0][2] == 'O' && game.a[1][1] == 'O' && game.a[2][0] == 'O') || (game.a[0][0] == 'O' && game.a[1][0] == 'O' && game.a[2][0] == 'O') || (game.a[0][1] == 'O' && game.a[1][1] == 'O' && game.a[2][1] == 'O') || (game.a[0][2] == 'O' && game.a[1][2] == 'O' && game.a[2][2] == 'O') || (game.a[0][2] == 'O' && game.a[0][1] == 'O' && game.a[0][0] == 'O') || (game.a[1][2] == 'O' && game.a[1][1] == 'O' && game.a[1][0] == 'O') || (game.a[2][2] == 'O' && game.a[2][1] == 'O' && game.a[2][0] == 'O'))
        {
            if (game.a[0][0] == 'O' && game.a[1][1] == 'O' && game.a[2][2] == 'O')
            {
                game.b[0][0] = 1;
                game.b[1][1] = 1;
                game.b[2][2] = 1;
            }
            if (game.a[0][2] == 'O' && game.a[1][1] == 'O' && game.a[2][0] == 'O')
            {
                game.b[0][2] = 1;
                game.b[1][1] = 1;
                game.b[2][0] = 1;
            }
            if (game.a[0][0] == 'O' && game.a[1][0] == 'O' && game.a[2][0] == 'O')
            {
                game.b[0][0] = 1;
                game.b[1][0] = 1;
                game.b[2][0] = 1;
            }
            if (game.a[0][1] == 'O' && game.a[1][1] == 'O' && game.a[2][1] == 'O')
            {
                game.b[0][1] = 1;
                game.b[1][1] = 1;
                game.b[2][1] = 1;
            }
            if (game.a[0][2] == 'O' && game.a[1][2] == 'O' && game.a[2][2] == 'O')
            {
                game.b[0][2] = 1;
                game.b[1][2] = 1;
                game.b[2][2] = 1;
            }
            if (game.a[0][0] == 'O' && game.a[0][1] == 'O' && game.a[0][2] == 'O')
            {
                game.b[0][0] = 1;
                game.b[0][1] = 1;
                game.b[0][2] = 1;
            }
            if (game.a[1][0] == 'O' && game.a[1][1] == 'O' && game.a[1][2] == 'O')
            {
                game.b[1][0] = 1;
                game.b[1][1] = 1;
                game.b[1][2] = 1;
            }
            if (game.a[2][0] == 'O' && game.a[2][1] == 'O' && game.a[2][2] == 'O')
            {
                game.b[2][0] = 1;
                game.b[2][1] = 1;
                game.b[2][2] = 1;
            }

            game.player1_win = true;
            if (frame<=0)
            game.player1_win_counter++;
            frame++;
            if (frame == 1)
            PlaySound(win);
        }
        else if ((game.a[0][0] == 'X' && game.a[1][1] == 'X' && game.a[2][2] == 'X') || (game.a[0][2] == 'X' && game.a[1][1] == 'X' && game.a[2][0] == 'X') || (game.a[0][0] == 'X' && game.a[1][0] == 'X' && game.a[2][0] == 'X') || (game.a[0][1] == 'X' && game.a[1][1] == 'X' && game.a[2][1] == 'X') || (game.a[0][2] == 'X' && game.a[1][2] == 'X' && game.a[2][2] == 'X') || (game.a[0][2] == 'X' && game.a[0][1] == 'X' && game.a[0][0] == 'X') || (game.a[1][2] == 'X' && game.a[1][1] == 'X' && game.a[1][0] == 'X') || (game.a[2][2] == 'X' && game.a[2][1] == 'X' && game.a[2][0] == 'X'))
        {
            if (game.a[0][0] == 'X' && game.a[1][1] == 'X' && game.a[2][2] == 'X')
            {
                game.b[0][0] = 1;
                game.b[1][1] = 1;
                game.b[2][2] = 1;
            }
            if (game.a[0][2] == 'X' && game.a[1][1] == 'X' && game.a[2][0] == 'X')
            {
                game.b[0][2] = 1;
                game.b[1][1] = 1;
                game.b[2][0] = 1;
            }
            if (game.a[0][0] == 'X' && game.a[1][0] == 'X' && game.a[2][0] == 'X')
            {
                game.b[0][0] = 1;
                game.b[1][0] = 1;
                game.b[2][0] = 1;
            }
            if (game.a[0][1] == 'X' && game.a[1][1] == 'X' && game.a[2][1] == 'X')
            {
                game.b[0][1] = 1;
                game.b[1][1] = 1;
                game.b[2][1] = 1;
            }
            if (game.a[0][2] == 'X' && game.a[1][2] == 'X' && game.a[2][2] == 'X')
            {
                game.b[0][2] = 1;
                game.b[1][2] = 1;
                game.b[2][2] = 1;
            }
            if (game.a[0][0] == 'X' && game.a[0][1] == 'X' && game.a[0][2] == 'X')
            {
                game.b[0][0] = 1;
                game.b[0][1] = 1;
                game.b[0][2] = 1;
            }
            if (game.a[1][0] == 'X' && game.a[1][1] == 'X' && game.a[1][2] == 'X')
            {
                game.b[1][0] = 1;
                game.b[1][1] = 1;
                game.b[1][2] = 1;
            }
            if (game.a[2][0] == 'X' && game.a[2][1] == 'X' && game.a[2][2] == 'X')
            {
                game.b[2][0] = 1;
                game.b[2][1] = 1;
                game.b[2][2] = 1;
            }
            game.player2_win = true;
            if (frame<=0)
            game.player2_win_counter++;
            frame++;
            if (frame == 1)
            PlaySound(win);
        }
        else if (!game.player1_win && !game.player2_win && game.turn == 9)
        {
            game.draw = true;
            if (frame<=0)
            game.draw_counter++;
            frame++;
        }

        // دکمه‌ها و کلیدها
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT) && mouse.x >= width/2 - 30 && mouse.x <= width/2 + 50 && mouse.y >= 300 && mouse.y<=335 && !human && !user && !theme && !question)
        {
            close_window = false;
            PlaySound(button);
        }
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT) && mouse.x >= width/2 - 50 && mouse.x <= width/2 + 70 && mouse.y >= 150 && mouse.y<=185 && !human && !user && !theme && !question && game.player1_name_is_changed && game.player2_name_is_changed)
        {
            human = true;
            PlaySound(button);
        }
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT) && mouse.x >= 5 && mouse.x <= 45 && mouse.y >= 355 && mouse.y<=395 && !human && !theme && !question && !user)
        {
            user = true;
            PlaySound(button);
        }
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT) && mouse.x >= 5 && mouse.x <= 45 && mouse.y >= 315 && mouse.y<=355 && !human && !user && !theme && !question)
        {
            question = true;
            PlaySound(button);
        }
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT) && mouse.x >= 5 && mouse.x <= 45 && mouse.y >= 315 && mouse.y<=355 && (human))
        {
            restart = true; // در مود بازی انسانی
            PlaySound(button);
        }
        if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT) && mouse.x >= 5 && mouse.x <= 45 && mouse.y >= 355 && mouse.y<=395 && (human || user_tmp || theme || question))
        {
            human = false;
            user = false;
            theme = false;
            question = false;
            PlaySound(button);
        }

        user_tmp = user; //برای تعمیر بخش کاربر و خروج
        

        EndDrawing();

    }

    // دانلود تصاویر از جی پی یو
    UnloadTexture(texture5);
    UnloadTexture(texture4);
    UnloadTexture(texture3);
    UnloadTexture(texture2);
    UnloadTexture(texture1);
    UnloadTexture(texture);

    UnloadSound(button);
    UnloadSound(win);
    UnloadSound(placing);
    CloseAudioDevice();

    CloseWindow();

}
