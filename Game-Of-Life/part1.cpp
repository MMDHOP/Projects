#include <iostream>
#include <thread>
#include <chrono>
#include <cstdlib> 
using namespace std;

int main() 
{
    char jad[10][15];
    int val[10][15];


    for (int i = 0; i < 10; i++) {
        for (int j = 0; j < 15; j++) {
            cin >> jad[i][j];
            if (jad[i][j] == '@')
                val[i][j] = 1;
            else if (jad[i][j] == '#')
                val[i][j] = 0;
        }
    }


    for (int step = 0; step < 3; step++) {
        int newVal[10][15]; 


        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 15; j++) {
                int neighbors = 0;

                if (i > 0) neighbors += val[i-1][j];
                if (i < 9) neighbors += val[i+1][j];
                if (j > 0) neighbors += val[i][j-1];
                if (j < 14) neighbors += val[i][j+1];


                if (neighbors > 1)
                    newVal[i][j] = 1;
                else
                    newVal[i][j] = 0;
            }
        }


        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 15; j++) {
                val[i][j] = newVal[i][j];
                jad[i][j] = (val[i][j] == 1) ? '@' : '#';
            }
        }


        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 15; j++) {
                cout << jad[i][j] << ' ';
            }
            cout << endl;
        }


        this_thread::sleep_for(chrono::seconds(2));
        if (step!=2)
            system("cls");
    }

    return 0;
}
