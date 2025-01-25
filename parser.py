import math
import typing as ty


class Parser:
    def __init__(self) -> None:
        self.src = ''
        self.char = ''
        self.pos = -1
        self._readChar()
    
    def _readChar(self) -> None:
        if self.pos < len(self.src)-1:
            self.pos += 1
            self.char = self.src[self.pos]
        else:
            self.char = '\0'
    
    def _peekChar(self) -> str:
        if self.pos < len(self.src)-1:
            return self.src[self.pos+1]
        return '\0'
    
    def _readUnquotedArg(self) -> str:
        startPos = self.pos
        while not self.char.isspace():
            self._readChar()
            if self.char == '\0':
                return self.src[startPos:self.pos+1]
        return self.src[startPos:self.pos]
    
    def _readQuotedArg(self, quote: str) -> str:
        startPos = self.pos
        self._readChar()
        while self.char != quote:
            if self.char == '\0':
                return self.src[startPos+1:self.pos+1]
            self._readChar()
        return self.src[startPos+1:self.pos]

    def _readPosData(self) -> list[float] | int:
        startPos = self.pos
        self._readChar()
        while self.char != ')':
            self._readChar()
        all = [i.strip() for i in self.src[startPos+1:self.pos].split(',')]
        if len(all) != 2:
            return 1
        try:
            return [float(i) for i in all]
        except ValueError:
            return 2
    
    def _readVelData(self) -> list[float] | int:
        startPos = self.pos
        self._readChar()
        while self.char != ']':
            self._readChar()
        all = [i.strip() for i in self.src[startPos+1:self.pos].split(',')]
        if len(all) != 2:
            return 1
        try:
            return [float(i) for i in all]
        except ValueError:
            return 2
    
    def _readOpt(self) -> str:
        startPos = self.pos
        self._readChar()
        while not self.char.isspace():
            if self.char == '\0':
                return self.src[startPos+1:self.pos+1]
            self._readChar()
        return self.src[startPos+1:self.pos]
    
    def _readComm(self) -> str:
        startPos = self.pos
        while not self.char.isspace():
            if self.char == '\0':
                return self.src[startPos:self.pos+1]
            self._readChar()
        return self.src[startPos:self.pos]

    def parse(self) -> ty.Any:
        args: dict[int, str]
        opts: dict[int, str]
        self.src  = self.src.strip()
        command = ''
        args = {}
        opts = {}
        allPos = {}
        allVel = {}
        count = 0
        self.char = ''
        self.pos = -1
        self._readChar()

        command = self._readComm()
        
        while self.char != '\0':
            if self.char.isspace():
                self._readChar()
                continue
            
            elif (temp := (self.char == '\'')) or self.char ==  '"':
                arg = self._readQuotedArg('\'' if temp else '"')
                args[count] = arg
            
            elif self.char == '-' and not self._peekChar().isspace() \
                    and self._peekChar() != '\0':
                opt = self._readOpt()
                opts[count] = opt
            
            elif self.char == '(':
                allPos[count] = (self._readPosData())
            
            elif self.char == '[':
                allVel[count] = (self._readVelData())
            
            elif self.char != ' ':
                arg = self._readUnquotedArg()
                args[count] = arg
            
            count += 1
            self._readChar()
        
        return command, args, opts, allPos, allVel
