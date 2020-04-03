def generate_sequence(states, sequence_length):
    
    all_sequences = []
    nodes = []
    
    depth = sequence_length
    
    def gen_seq_recur(states,nodes,depth):
        if depth == 0:
            #print nodes
            all_sequences.append(nodes)
        else:
            for state in states:
                temp_nodes = list(nodes)
                temp_nodes.append(state)
                gen_seq_recur(states,temp_nodes,depth-1)
    
    gen_seq_recur(states,[],depth)
                
    return all_sequences


def score_sequences(sequences,initial_probs,transition_probs,emission_probs,obs):
    
    best_score = -1
    best_sequence = None
    
    sequence_scores = []
    for seq in sequences:
        total_score = 1
        total_score_breakdown = []
        first = True
        for i in range(len(seq)):
            state_score = 1
            # compute transitition probability score
            if first == True:
                state_score *= initial_probs[seq[i]]
                # reset first flag
                first = False
            else:  
                state_score *= transition_probs[seq[i] + "|" + seq[i-1]]
            # add to emission probability score
            state_score *= emission_probs[obs[i] + "|" + seq[i]]
            # update the total score
            #print state_score
            total_score_breakdown.append(state_score)
            total_score *= state_score
            
        sequence_scores.append(total_score)
        
    return sequence_scores
# pretty printing our  distributions
# from sets import Set
import pandas as pd
from tabulate import tabulate
def pretty_print_probs(distribs):
    
    rows = set()
    cols = set()
    for val in distribs.keys():
        temp = val.split("|")
        rows.add(temp[0])
        cols.add(temp[1])
        
    rows = list(rows)
    cols = list(cols)
    df = []
    for i in range(len(rows)):
        temp = []
        for j in range(len(cols)):
            temp.append(distribs[rows[i]+"|"+cols[j]])
            
        df.append(temp)
        
    I = pd.Index(rows, name="rows")
    C = pd.Index(cols, name="cols")
    df = pd.DataFrame(data=df,index=I, columns=C)
    
    print (tabulate(df, headers='keys', tablefmt='psql'))

def initializeSequences(_obs):
    # Generate list of sequences
    
    seqLen = len(_obs)
    seqs = generate_sequence(states,seqLen)
    print(seqs)
    # Score sequences
    seq_scores = score_sequences(seqs,initial_probs,transition_probs,emission_probs,obs)
    
    return (seqLen,seqs,seq_scores)


# We can use a dictionary to capture our state transitions
# set of hidden states
states = ['A','B']
# set of observations
obs = ['Red','Green','Red']
# initial state probability distribution (our priors)
initial_probs = {'A':1.0,'B':0.0}
# transition probabilities
transition_probs = {'A|A':0,'A|B':1,'B|A':1,'B|B':0}
# emission probabilities
emission_probs = {'Red|A':1,'Green|A':0,'Red|B':0.25,'Green|B':0.75}
# Generate list of sequences
sequence_length,sequences,sequence_scores = initializeSequences(obs)

print("Initial Distributions")
print (initial_probs)

print("\nTransition Probabilities")
pretty_print_probs(transition_probs)

print("\nEmission Probabilities")
pretty_print_probs(emission_probs)

print("\nScores")
# Display sequence scores
for i in range(len(sequences)):
    print("Sequence:%10s,Score:%0.4f" % (sequences[i],sequence_scores[i]))
