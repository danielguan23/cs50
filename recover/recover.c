#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //open file and errors
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    else
    {
        char *inputfile = argv[1];
        FILE *file = fopen(inputfile, "r");

        if (file == NULL)
        {
            printf("Error: cannot open %s\n", inputfile);
            return 1;
        }

        BYTE buffer[512];
        int counter = 0;
        FILE *imgpointer = NULL;
        char filename[8];

        //read card
        while (fread(buffer, 512, 1, file) == 1)
        {
            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
            {
                if (!(counter == 0))
                {
                    fclose(imgpointer);
                }
                sprintf(filename, "%03i.jpg", counter);
                imgpointer = fopen(filename, "w");
                counter++;

            }
            if (!(counter == 0))
            {
                fwrite(buffer, 512, 1, imgpointer);
            }
        }
        fclose(file);
        fclose(imgpointer);
        return 0;
    }

}
