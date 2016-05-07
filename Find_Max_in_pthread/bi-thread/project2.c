/*****************************************/
/* pthread barrier for synchronization   */
/*****************************************/
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <stdbool.h>
#define threadNum 2048


/*BARRIER_FLAG =INF  unsigned long 2^31*/
#define BARRIER_FLAG (1UL<<30)
//#define PTHREAD_BARRIER_SERIAL_THREAD 1


//let user-defined function replace the default
#define pj2_pthread_barrier_init(B, A, N) (barrier_init_pj2((B), (N)), 0)
#define pj2_pthread_barrier_destroy(B) (barrier_destroy_pj2(B), 0)
#define pj2_pthread_barrier_wait barrier_wait_pj2
//barrier
typedef struct barrier_pj2_ barrier_pj2;

struct barrier_pj2_
{
	unsigned count;
	unsigned total;
	pthread_mutex_t m;
	pthread_cond_t cv;
};

static int *array;  //current array
static int *array_temp;  //to store our maximum value

static barrier_pj2 barr;  // barrier variable

typedef struct  // to pass parameters
{
	int start;
	int end;
}_parameter_;
_parameter_ *para[threadNum];

int arraySize=0;

pthread_mutex_t lock;


void readArray(char *fileName){
	FILE *fp;
	char c;
	int i=0,len1,len2;
	fp=fopen(fileName,"r");
	if(!fp){
	printf("Invaild file %s \n",fileName);
	exit;
    }
    fseek(fp, 0L, SEEK_END);
    len1 = ftell(fp);
    fseek(fp, 0L, SEEK_SET);
    len2 = ftell(fp);
   while(len2 != len1)
   {
	fscanf(fp," %d",&array[i]); i++;
   	len2 = ftell(fp);
   }
   fclose(fp);
   arraySize=i;

}

static void barrier_destroy_pj2(barrier_pj2 *b);
static void barrier_init_pj2(barrier_pj2 *b, unsigned count);
static  int barrier_wait_pj2(barrier_pj2 *b);



void *findMax(void *para){
	int start,end,i,j;
	int maxValue=0;

	_parameter_ *para_=para;
	start=para_->start;
	end=para_->end;
	for(i = start; i <= end; i++)
	{
		if(array[i] > maxValue)
		{
			maxValue = array[i];
		}
	}
	j=start/(end-start+1);
	array_temp[j]=maxValue;

    pj2_pthread_barrier_wait(&barr);
}

int main(int argc,char *argv[]){
	int i,j,k,*temp;
	pthread_t tid[threadNum];			// to store the id of each threads.
	pthread_mutex_init(&lock,NULL);		// initiate the mutex.
    array=malloc(threadNum*2*sizeof(int));
    array_temp=malloc(threadNum*sizeof(int));
    
	if (argc!= 2)
    {
	printf("Not enough args :( Process terminated!\n");
	exit(1);
    }

    if (strcmp(argv[1],"inData.txt")!=0)
    {
	printf("Incorrect file name :( Process terminated!\n");
	exit(1);
    }
	readArray("inData.txt");

	if(arraySize!=0)
	{
		i=arraySize/2;
		while(1)
		{
			j=arraySize/i;
			if(pj2_pthread_barrier_init(&barr,NULL,i+1))
			{
				printf("Error, Cannot initialize barrier\n");
				return -1;
			}
			for(k=0;k<i;k++)
			{
				para[k]=(_parameter_*)malloc(sizeof(_parameter_));
				para[k]->start=k*j;
				para[k]->end=(k+1)*j-1;
				if(pthread_create(&tid[k],NULL,findMax,para[k])){
					printf("Cannot not create thread\n");
					return -1;
				}
			}
			pj2_pthread_barrier_wait(&barr);
			pj2_pthread_barrier_destroy(&barr);
			for(k=0;k<i;k++)free(para[k]);
            temp=array_temp;
            array_temp=array;
            array=temp;
			if(i==1) break;
			else i=i/2;
		}
	printf("The largest integer is %d\n",array[0]);
	}
	else
	{
		printf("Empty file!\n");
		
	}
	pthread_mutex_destroy(&lock);


	return 0;
}




void barrier_destroy_pj2(barrier_pj2 *b)
{
    pthread_mutex_lock(&b->m);

    while (b->total > BARRIER_FLAG)
    {
        pthread_cond_wait(&b->cv, &b->m);
    }

    pthread_mutex_unlock(&b->m);

    pthread_cond_destroy(&b->cv);
    pthread_mutex_destroy(&b->m);
}

void barrier_init_pj2(barrier_pj2 *b, unsigned count)
{
    pthread_mutex_init(&b->m, NULL);
    pthread_cond_init(&b->cv, NULL);
    b->count = count;
    b->total = BARRIER_FLAG;
}

int barrier_wait_pj2(barrier_pj2 *b)
{
    pthread_mutex_lock(&b->m);
    
    if (b->total == BARRIER_FLAG) b->total = 0;
    b->total++;

    if (b->total == b->count)
    {
        b->total += BARRIER_FLAG - 1;
        pthread_cond_broadcast(&b->cv);

        pthread_mutex_unlock(&b->m);

        return PTHREAD_BARRIER_SERIAL_THREAD;
    }
    else
    {
        while (b->total < BARRIER_FLAG)
        {
            pthread_cond_wait(&b->cv, &b->m);
        }

        b->total--;
        if (b->total == BARRIER_FLAG) pthread_cond_broadcast(&b->cv);

        pthread_mutex_unlock(&b->m);

        return 0;
    }
}
