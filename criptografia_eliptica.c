#include <stdio.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>
#include <locale.h>
#include <windows.h>

// Struct b�sica com as duas chaves de cada usu�rio.
struct usuario{
    unsigned long long chave_privada;
    unsigned long long chave_publica;
};


unsigned long long geracao_numero_primo(long long); //Gera n n�meros primos a partir do 13
unsigned long long curva_eliptica(long long, long long); //curva Koblitz secp256k1 (y^2 = x^3 + 7) (utilizada no bitcoin)
unsigned long long geracao_chave_privada(); // A partir de uma seed, gera um n�mero aleat�rio que servir� de chave privada
unsigned long long geracao_chave_publica(long long, long long, long long); // A partir de um ponto base da curva el�ptica e a chave privada, gera uma chave p�blica
void criptografar(char[], long long, long long); // Recebe uma string (vetor de caracteres) e com base na chave privada do usu�rio que envia e a chave p�blica de quem recebe, criptografa a string recebida.
void descriptografar(char[], long long, long long); // Recebe uma mensagem j� criptografada e com base na chave p�blica do usu�rio que enviou a mensagem e a chave privada de quem recebeu, descriptografa a string recebida.


int main(void){
    setlocale(LC_ALL,"Portuguese"); //Fun��o para permitir o uso de acentua��o nos outputs.

    unsigned long long primo = geracao_numero_primo(100);

    srand(time(NULL));
    unsigned long long ponto_Gx = rand(); // valor x do ponto G da curva
    unsigned long long ponto_Gy = curva_eliptica(ponto_Gx, primo); // valor y do ponto G da curva

    struct usuario usuario1, usuario2;

    usuario1.chave_privada = geracao_chave_privada();
    usuario1.chave_publica = geracao_chave_publica(ponto_Gx, usuario1.chave_privada, primo);

    usuario2.chave_privada = geracao_chave_privada();
    usuario2.chave_publica = geracao_chave_publica(ponto_Gx, usuario2.chave_privada, primo);

    char mensagem_teste[] = "�Existem muitas hip�teses em ci�ncia que est�o erradas. Isso � perfeitamente aceit�vel, elas s�o a abertura para achar as que est�o certas�. (Carl Sagan)";

    printf("NUMERO PRIMO UTILIZADO: %d\n", primo);
    printf("Ponto G: (%d, %d)\n", ponto_Gx, ponto_Gy);
    printf("CHAVE PRIVADA USUARIO 1: %d\n", usuario1.chave_privada);
    printf("CHAVE PUBLICA USUARIO 1: %d\n", usuario1.chave_publica);
    printf("CHAVE PRIVADA USUARIO 2: %d\n", usuario2.chave_privada);
    printf("CHAVE PUBLICA USUARIO 2: %d\n\n\n", usuario2.chave_publica);
    printf("MENSAGEM ORIGINAL:\n%s\n\n", mensagem_teste); //Primeiro print da string mensagem_teste.

    criptografar(mensagem_teste, usuario1.chave_privada, usuario2.chave_publica);
    printf("MENSAGEM P�S CRIPTOGRAFIA:\n%s\n\n", mensagem_teste); // Segundo print da string mensagem_teste.
    descriptografar(mensagem_teste, usuario1.chave_publica, usuario2.chave_privada);
    printf("MENSAGEM P�S DESCRIPTOGRAFIA:\n%s\n", mensagem_teste); // Terceiro print da string mensagem_teste.

    return 0;
}


unsigned long long curva_eliptica(long long x, long long primo){   //Para um valor de x, retorna o valor de y da curva el�ptica
    x = pow(pow(x, 3) + 7, 0.5);

    return x%primo;
}


unsigned long long geracao_chave_privada(){ // Gera um valor aleat�ria, com base em uma semente, que ser� usado como chave privada
    Sleep(1100);
    srand(time(NULL));
    return rand();

}


unsigned long long geracao_chave_publica(long long ponto_base, long long chave_privada, long long primo){ // gera um n�mero a partir do ponto base pr� definido e a chave privada do usu�rio.
    int v = 0;
    while (v == 0){
        v = chave_privada*curva_eliptica(ponto_base, primo);
    }

    return chave_privada*curva_eliptica(ponto_base, primo);
}


void criptografar(char mensagem_original[], long long chave_privada1, long long chave_publica2){
    if (mensagem_original[0] != '\0'){
        mensagem_original[0] = mensagem_original[0] + chave_privada1*chave_publica2;
        return criptografar(mensagem_original+1, chave_privada1, chave_publica2);
    }
}


void descriptografar(char mensagem_criptografada[], long long chave_publica1, long long chave_privada2){
    if (mensagem_criptografada[0] != '\0'){
        mensagem_criptografada[0] = mensagem_criptografada[0] - chave_privada2*chave_publica1;
        return descriptografar(mensagem_criptografada+1, chave_privada2, chave_publica1);
    }
}


unsigned long long geracao_numero_primo(long long qtd){
    long long primos[qtd];
    long long gerados = 0;
    long long valor_teste = 13; //Inicia pelo 13 pois valores menores podem gerar chaves que n�o possibilitaram os c�lculos corretos acontecerem
    bool primo;

    while(gerados < qtd){
        primo = true;
        for (int i = 2; i < sqrt(valor_teste)+1; i ++){
            if(valor_teste%i == 0 || valor_teste%2 == 0){
                primo = false;
                break;
            }
        }
        if (primo){
            primos[gerados] = valor_teste;
            gerados++;
        }
        valor_teste++;
    }

    srand(time(NULL));
    long long index = rand()%gerados;

    return primos[index];
}

