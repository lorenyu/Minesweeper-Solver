class DeterministicFiniteAutomata:

    def __init__(self, states, alphabet, transitions, startState, acceptStates):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.startState = startState
        self.acceptStates = acceptStates
        
        # initialize current state to start state
        self.state = startState
        
    def reset(self):
        self.state = self.startState
    
    def transition(self, symbol):
        self.state = self.transitions[self.state][symbol]
        
    def accept(self):
        return self.state in self.acceptStates
        
class SequenceAutomata(DeterministicFiniteAutomata):

    def __init__(self, sequence, alphabet = None):
        self.sequence = sequence
    
        if alphabet == None:
            alphabet = set(sequence)

        states = range(-1, len(sequence))
        transitions = {}
        for state in states:
            nextStates = {}
            for symbol in alphabet:
                nextStates[symbol] = SequenceAutomata._NextState(sequence, state, symbol)
            transitions[state] = nextStates
        
        n = len(sequence)
        DeterministicFiniteAutomata.__init__(self, states, alphabet, transitions, -1, set([n - 1]))
        
    def _NextState(sequence, index, symbol):
        '''Given a sequence 'S', the index of the current state in that sequence 'i', and the next symbol 'a',
        find the longest prefix of the sequence that is a suffix of the symbols.
        Equivalently, find longest suffix of symbols that is a prefix of the sequence.
        Find smallest i such that sequence[i:index + 1]+[symbol] == sequence[0:index+1-i]'''
        
        if index == -1:
            symbols = [symbol]
        else:
            symbols = sequence[0:index + 1] + [symbol]
        n = len(symbols)
        for i in range(0, n):
            if symbols[i:n] == sequence[0:n - i]:
                return n - i - 1
        return -1
    _NextState = staticmethod(_NextState)
        
#class EventSequenceMachine(StateMachine):

    #def __init__(self, alphabet, sequence, eventMap = lambda x: x):
        
        #pass
        #StateMachine.__init__(self, alphabet, , )

if __name__ == '__main__':
    print 'type "quit" to quit'

    a, b, c = 'a', 'b', 'c'
    sequence = [a,b,c,a,b,c,a,b,a,c]
    alphabet = set([a,b,c])
    print 'sequence =', sequence
    print 'alphabet =', alphabet
    DFA = SequenceAutomata(sequence, alphabet)
    s = ''
    while True:
        accept = ''
        if DFA.accept():
            accept = '(accepting)'
        print 'current state =', DFA.state, accept
        s = raw_input()
        if s == 'quit':
            break
        DFA.transition(s)
