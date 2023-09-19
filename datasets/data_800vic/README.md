# DESCRIÇÃO DO DATASET
Data de criação: 12/9/2023  
Script MatLab  
Autor: Cesar Augusto Tacla  

## ATRIBUTOS
- id: número sequencial; Inteiro [1, <número de vítimas>]
- pSist: pressão sistólica; Real [5, 22]
- pDiast: pressão diastólica; Real [0, 15]
- qPA: qualidade da pressão arterial (gerado a partir de pSist e pDiast); Real [-10, 10] sendo -10 a pior qualidade e +10, a melhor.
- pulso: pulsação; Real [0, 200] BPM
- fResp: frequência respiratória; Real [0, 22] freq. respiratória por minuto
- grav: gravidade da vítima de 0 a 100, sendo 100 a MENOS GRAVE; Real [0, 100]
- label: 1=CRÍTICO 2=INSTÁVEL 3=POTENCIALMENTE INSTÁVEL 4=ESTÁVEL; Inteiro [1, 4]

## ARQUIVOS 
1) sinais_vitais_com_label.txt  
   Atributos: [id, pSist, pDiast, qPA, pulso, fResp, grav, label]

2) sinais_vitais_sem_label.txt  
Atributos: [id, pSist, pDiast, qPA, pulso, resp, grav]

### CONTAGENS
São idênticas para os dois arquivos:  

1=critico.....: 119 (14.875%)  
2=instável....: 455 (56.875%)  
3=pot. estável: 211 (26.375%)  
4=estavel.....: 15  ( 1.875%)  
