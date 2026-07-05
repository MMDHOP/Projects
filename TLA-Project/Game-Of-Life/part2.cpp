#include <iostream>
using namespace std;

// ساختار برای ذخیره مختصات (ردیف و ستون)
struct Position
{
    int row, col; // مختصات در ماتریس
};

int main()
{
    const int ROWS = 10;
    const int COLS = 15;

    // تعریف ماتریس
    char grid[ROWS][COLS] =
        {
            {'#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'},
            {'@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@'},
            {'@', '@', '@', '#', '#', '#', '#', '#', '#', '#', '@', '@', '@', '#', '#'},
            {'@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@'},
            {'#', '#', '@', '#', '#', '#', '#', '#', '#', '#', '#', '#', '@', '#', '#'},
            {'#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'},
            {'@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@'},
            {'@', '@', '@', '#', '#', '#', '#', '#', '#', '#', '@', '@', '@', '#', '#'},
            {'@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@', '#', '@'},
            {'#', '#', '@', '#', '#', '#', '#', '#', '#', '#', '#', '#', '@', '#', '#'}};

    // تعریف صف برای BFS
    int queue[ROWS * COLS][2]; // آرایه‌ای برای نگهداری مختصات خانه‌ها
    int front = 0, rear = 0;   // اشاره‌گرهای صف

    // آرایه بازدید
    bool visited[ROWS][COLS] = {false};

    // آرایه والد برای بازسازی مسیر
    Position parent[ROWS][COLS];

    // گرفتن مختصات شروع و پایان
    int startRow, startCol, endRow, endCol;

    cin >> startRow >> startCol;
    cin >> endRow >> endCol;

    // مقداردهی اولیه والد نقطه شروع
    parent[startRow][startCol] = {-1, -1};

    // اضافه کردن نقطه شروع به صف
    queue[rear][0] = startRow;
    queue[rear][1] = startCol;
    rear++;
    visited[startRow][startCol] = true;

    // جهت‌های چهارگانه
    int dRow[] = {-1, 1, 0, 0};
    int dCol[] = {0, 0, -1, 1};

    bool found = false;

    // BFS
    while (front < rear && !found)
    {
        // برداشتن خانه از صف
        int row = queue[front][0];
        int col = queue[front][1];
        front++;

        // بررسی خانه‌های مجاور
        for (int i = 0; i < 4; i++)
        {
            int newRow = row + dRow[i];
            int newCol = col + dCol[i];

            // بررسی محدوده و بازدید نشده و قابل‌عبور بودن
            if (newRow >= 0 && newRow < ROWS && newCol >= 0 && newCol < COLS &&
                !visited[newRow][newCol] && grid[newRow][newCol] == '#')
            {
                queue[rear][0] = newRow;
                queue[rear][1] = newCol;
                rear++;
                visited[newRow][newCol] = true;
                parent[newRow][newCol] = {row, col}; // ذخیره والد

                // بررسی رسیدن به مقصد
                if (newRow == endRow && newCol == endCol)
                {
                    found = true;
                    break;
                }
            }
        }
    }

    // بررسی وجود مسیر
    if (!found)
    {
        cout << "No path exists between the start and end points.\n";
    }
    else
    {
        // بازسازی مسیر
        Position path[ROWS * COLS]; // مسیر به صورت آرایه‌ای
        int pathLength = 0;

        for (Position at = {endRow, endCol}; at.row != -1 && at.col != -1; at = parent[at.row][at.col])
        {
            path[pathLength] = at;
            pathLength++;
        }

        // چاپ مسیر
        cout << "Path from start to end:\n";
        for (int i = pathLength - 1; i >= 0; i--)
        {
            cout << "(" << path[i].row << ", " << path[i].col << ")";
            if (i > 0)
                cout << " -> ";
        }
        cout << endl;

        // نمایش ماتریس همراه مسیر
        for (int i = 0; i < ROWS; i++)
        {
            for (int j = 0; j < COLS; j++)
            {
                bool isInPath = false;
                for (int k = 0; k < pathLength; k++)
                {
                    if (path[k].row == i && path[k].col == j)
                    {
                        isInPath = true;
                        break;
                    }
                }
                if (isInPath)
                    cout << '*'; // نمایش مسیر با '*'
                else
                    cout << grid[i][j];
                cout << ' ';
            }
            cout << endl;
        }
    }

    return 0;
}
