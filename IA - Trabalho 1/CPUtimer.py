# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 12:20:30 2016

@author: Rafael França ( psyny.rafael@gmail.com )
"""

import platform
import time
import timeit

class CPUTimer:
    """
    Mede e armazena o tempo de CPU para operações.
    """
    # Variaveis Internas
    times = list()
    start_mark = 0
    avarage = 0
    total = 0
    last = 0
    detail_level = 0
    sensor = time.time
    
    # Incializador / Construtor da classe
    def __init__(self , detail_level = 0 ):
        """
        detail_level = 0:
            não armazena o tempo individual de cada cronometragem
            
        detail_level = 1:
            armazena o tempo individual de cada cronometragem
        """
        if platform.system() == "Windows":
            self.sensor = time.clock
        self.reset()
        self.detail_level = detail_level
     
     
    def start(self):
        """
        Inicia a medição/cronometragem
        
        Retorna: nada
        """        
        if self.start_mark == 0:
            self.start_mark = self.sensor()
        
        
    def stop(self):
        """
        Pausa a medição/cronometragem
        
        Retorna: nada
        """         
        if self.start_mark != 0:
            
            # Checa nivel de detalhe da medição
            if self.detail_level > 0:
                self.times[-1] = self.times[-1] + ( self.sensor() - self.start_mark )
                
            else:
                # Detail level = 0
                self.last = self.sensor() - self.start_mark
                self.total = self.total + self.last
                
                if self.avarage > 0:
                    self.avarage = ( self.avarage + self.last ) / 2
                else:
                    self.avarage = self.last
                    
            self.start_mark = 0
        
        
    def lap(self, start_stopped = False ):
        """
        Para a medição/cronometragem atual e inicia uma nova.
        
        start_stopped = "FALSE":
            Imediamente inicia a nova cronometragem
        start_stopped != "FALSE":
            A nova cronometragem inicia-se pausada
            
        Retorna: nada
        """  
        self.stop()
        
        # Checa nivel de detalhe da medição
        if self.detail_level > 0:
            self.times.append(0)
        
        # Reinicia a medição
        if start_stopped == False:
            self.start()


    def reset(self):
        """
        Reseta variaveis internas e prepara instância da classe para uma
        nova bateria de cronometragems
        
        Retorna: nada
        """        
        del self.times[:]
        self.times.append(0)
        self.start_mark = 0
        self.avarage = 0
        self.total = 0
        self.last = 0
            

    def get_time(self, reference = "total", unit = "seconds" ):
        """
        Retorna a cronometragem armazenada de acordo com a referência e
        unidade requerida.
        
        reference = "total" ou "t":
            tempo total
        reference = "average" ou "avg" ou "a":
            tempo médio
        reference = "last" ou "l":
            tempo da última medição
        reference = "first" ou "f":
            para detail_level > 0, tempo da primeira medição
        reference = <inteiro>
            para detail_level > 0, tempo da medição de numero <inteiro>
            
        unit = "seconds" ou "sec" ou "s":
            retorna a medição em segundos
        unit = "minutes" ou "min" ou "m":
            retorna a medição em minutos
        unit = "hours" ou "hr" ou "h":
            retorna a medição em horas
        unit = "milliseconds" ou "millisec" ou "milli" ou "ms":
            retorna a medição em mili segundos
        unit = "microseconds" ou "microsec" ou "micro" ou "us":
            retorna a medição em micro segunds         
            
        Retorna: valor da medição requerida em float    
        """          
        
        # Salva o estado do relogio ( parado ou contando )
        state = self.start_mark
        self.stop()                
            
        # Salva ultimo elemento 
        if self.detail_level > 0:
            lastTime = self.times.pop()
            ret = lastTime
        
        # Calculo do tipo de retorno: tempo total, ultima marcacao, media
        if reference == "total" or reference == "t":
            if self.detail_level > 0:
                for t in self.times:
                    ret = ret + t                 
            else:
                ret = self.total
                
        elif reference == "average" or reference == "avg" or reference == "a":
            if self.detail_level > 0:
                for t in self.times:
                    ret = ( ret + t ) / 2
            else:
                ret = self.avarage
            
        elif reference == "last" or reference == "l":
            if self.detail_level > 0:
                ret = ret
            else:
                ret = self.last
        
        elif reference == "first" or reference == "f":
            if self.detail_level > 0:
                ret = self.times[0]
            else:
                ret = -1
            
        else:
            if self.detail_level > 0:
                ret = self.times[int(reference)]
            else:
                ret = -1
                
        # Calculo da unidade desejada
        if unit == "seconds" or unit == "sec" or unit == "s":
            ret = ret
        
        elif unit == "minutes" or unit == "min" or unit == "m":
            ret = ret / 60

        elif unit == "hours" or unit == "hr" or unit == "h":
            ret = ret / 60 / 60
            
        elif unit == "milliseconds" or unit == "millisec" or unit == "milli" or unit == "ms":
            ret = ret * 1000    
            
        elif unit == "microseconds" or unit == "microsec" or unit == "micro" or unit == "us":
            ret = ret * 1000 * 1000  
            
        elif unit == "stamp":
            stamp = ""
            stamp = stamp + str(int(ret/60/60)).zfill(2) + ":"
            stamp = stamp + str(int(ret/60)).zfill(2) + ":"
            stamp = stamp + str(int(ret)).zfill(2) + "."
            stamp = stamp + str(int(ret*1000)).zfill(4)
            ret = stamp
            
        # Repoe o elemento retirado
        if self.detail_level > 0:
            self.times.append(lastTime)
        
        # Retorna o relogio para o estado de antes da chamada da função
        if state != 0:
            self.start()
        
        # Retorna valor
        return ret
        
        
    def get_stamp(self, reference = "total" , style = "clock" , ignore_zeroes = False ):
        """
        Retorna um string da estampa de tempo de uma cronometragem de
        acordo com uma referencia e um estilo definido.
        
        reference = "total" ou "t":
            tempo total
        reference = "average" ou "avg" ou "a":
            tempo médio
        reference = "last" ou "l":
            tempo da última medição
        reference = "first" ou "f":
            para detail_level > 0, tempo da primeira medição
        reference = <inteiro>
            para detail_level > 0, tempo da medição de numero <inteiro>
            
        style = "clock":
            formato:
            HH:mm:ss.SSSS
            Legenda:
            <horas>:<minutos>:<segundos>.<milisegundos>      
        style = "si" ou "SI":
            formato:
            <hora>h <minuto>m <segundo>s <milisegundo>ms <microsegundo>us
            
        ignore_zeroes = False:
            Retorna todas as unidades de tempo 
        ignore_zeroes = True:
            Não retorna unidades de tempo iguais a zero
            
        Retorna: string da estampa de tempo
        """
        measure = self.get_time(reference, unit="s" )
        h = int(measure / 60 / 60)
        measure = (measure - (h*60*60))
        m = int(measure / 60)
        measure = (measure - (m*60))
        s = int(measure)
        measure = (measure - s)
        ms = int(measure*1000)
        measure = (measure - (ms/1000))
        us = int(measure*1000*1000)
        
        stamp = ""
        
        if style == "clock":
            if ignore_zeroes == False or ignore_zeroes == True and h > 0:   
                stamp = stamp + str(int(h)).zfill(2) + ":"
            if ignore_zeroes == False or ignore_zeroes == True and m > 0:       
                stamp = stamp + str(int(m)).zfill(2) + ":"
            if ignore_zeroes == False or ignore_zeroes == True and s > 0:       
                stamp = stamp + str(int(s)).zfill(2) + "."
            stamp = stamp + str(int(ms)).zfill(4)
        elif style == "SI" or style == "si":
            if ignore_zeroes == False or ignore_zeroes == True and h > 0:
                stamp = stamp + str(int(h)) + "h "
            if ignore_zeroes == False or ignore_zeroes == True and m > 0:      
                stamp = stamp + str(int(m)) + "m "
            if ignore_zeroes == False or ignore_zeroes == True and s > 0:     
                stamp = stamp + str(int(s)) + "s "
            if ignore_zeroes == False or ignore_zeroes == True and ms > 0:     
                stamp = stamp + str(int(ms)) + "ms "
            stamp = stamp + str(int(us)) + "\u00B5s"
            
        return stamp
        
        
    def auto_loop(self, function, repetitions = 1000000 ):
        """
        Mede a função passada várias vezes seguidas
        Apenas um wrapper da timeit.timeit
        
        function = <nome da função>:
            Função a ser executada
            
        repetitions = <inteiro>:
            Quantidade de vezes a se executar a função
            
        Retorna: nada
        
        Obs.:
        A chamada dessa função automaticamente tornará o detail_level = 0
        """  
        
        # A função timeit não fornece informações o suficiente para um relatório detalhado
        self.reset()
        self.detail_level = 0
        
        # Chama e timeit e processa os resultados para adequar ao padrão deste modulo
        if repetitions > 1:
            self.total = timeit.timeit( stmt=function , number=(repetitions - 1) )
            self.last = timeit.timeit( stmt=function , number=1 )
        else:
            self.last = timeit.timeit( stmt=function , number=1 )
            self.total = 0
        
        self.total = self.total + self.last
        self.avarage = self.total / repetitions
        
        return
        



