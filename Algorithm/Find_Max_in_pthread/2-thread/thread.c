#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

static int arrSize;
#define MAXLEN 1024

struct StructMax {
    int iMax;
};

//init mutex
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

//declaration
void *thread_search_max(void *);
int read_file(const char *filename, int *arr);

int main(int argc, char **argv) {
    int arr[arrSize];
    if(argc != 2) {
        fprintf(stderr, "Usage: ./read <filename>\n");
        return -1;
    }
    arrSize = read_file(argv[1], arr);

    pthread_t tid;
    struct StructMax *st_main;
    struct StructMax *st_th;
    int FinalMax;

    st_main = malloc(sizeof(struct StructMax));
    if (st_main == NULL)
        return -1;

    pthread_create(&tid, NULL, thread_search_max, arr);

    //lock the mutex, in this section access to 'arr' is allowed
    pthread_mutex_lock(&mutex);
    st_main->iMax = arr[0];
    pthread_mutex_unlock(&mutex);

    for (int iCount = 1 ; iCount < arrSize / 2 ; iCount++) {
        //lock the mutex, in this section access to 'arr' is allowed
        pthread_mutex_lock(&mutex);
        if(arr[iCount] > st_main->iMax) {
            st_main->iMax = arr[iCount];
        }
        pthread_mutex_unlock(&mutex);
    }
    //join thread
    pthread_join(tid, (void **)&st_th);

    if (st_main->iMax >= st_th->iMax) {
        FinalMax = st_main->iMax;
    } else {
        FinalMax = st_th->iMax;
    }
    printf("Final Max: %d \n", FinalMax);
    free(st_th);
    free(st_main);

    return 0;
}

void *thread_search_max(void *para) {
    struct StructMax *st;
    int iCount;
    int *arr;

    arr = para;
    if(arr == NULL)
        return NULL;
    st = malloc(sizeof(struct StructMax));
    if(st == NULL)
        return NULL;

    //lock the mutex, in this section access to 'arr' is allowed
    pthread_mutex_lock(&mutex);
    st->iMax = arr[arrSize/2];
    pthread_mutex_unlock(&mutex);
    for(iCount = arrSize /  2 + 1 ; iCount < arrSize ; iCount++) {
        //lock the mutex, in this section access to 'arr' is allowed
        pthread_mutex_lock(&mutex);
        if (arr[iCount] > st->iMax) {
            st->iMax = arr[iCount];
        }
        pthread_mutex_unlock(&mutex);
    }
    pthread_exit((void *)st);
}

int read_file(const char *filename, int *arr) {
    FILE *file;
    int pos, temp, i;
    //open file
    file = fopen(filename, "r");
    if(NULL == file) {
        fprintf(stderr, "Open %s error\n", filename);
        return -1;
    }
    //get size of array
    char buffer[MAXLEN];
    fgets(buffer, 1024, file);
    arrSize = atoi(buffer);
    //get array from file
    pos = 0;
    for(i = 0; i < arrSize; i++) {
        fscanf(file, "%d", &arr[pos]);
        pos++;
    }
    fclose(file);
    return pos;
}