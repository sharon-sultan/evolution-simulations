from functools import partial
from matplotlib import rcParams
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import re
import streamlit as st

def generate_offspring(seed, mutation_rate_offspring, mutation_rate_digit, mutation_rate_digit_up, mutation_rate_digit_up_plus, mutation_rate_digit_down_minus, number_of_offsprings):
    offspring = []
    for _ in range(number_of_offsprings):
        rand_offspring = random.random()
        if rand_offspring < mutation_rate_offspring:
            mutated = []
            for digit in seed:
                rand_digit = random.random()
                if rand_digit < mutation_rate_digit:
                    if digit == '9':
                        new_digit = '8'
                    elif digit == '0':
                        new_digit = '1'
                    else:
                        rand_direction = random.random()
                        new_digit = int(digit)
                        if rand_direction < mutation_rate_digit_up:  
                            if digit == '8':
                              new_digit = new_digit + 1
                            else:
                              rand_jump = random.random()
                              if rand_jump < mutation_rate_digit_up_plus: # +1 or +2
                                new_digit = new_digit + 1
                              else:
                                new_digit = new_digit + 2
                        else:
                          if digit == '1':
                            new_digit = new_digit - 1
                          else:
                            rand_jump = random.random()
                            if rand_jump < mutation_rate_digit_down_minus: # -1 or -2
                              new_digit = new_digit - 1
                            else:
                              new_digit = new_digit - 2
                    mutated.append(str(new_digit))
                else:
                    mutated.append(digit)
            offspring.append("".join(mutated))
        else:
           offspring.append(seed)
    return offspring

def calculate_score(offspring, target):
    scores = []
    for number in offspring:
        score = sum(abs(int(digit1) - int(digit2)) for digit1, digit2 in zip(str(number), target))
        scores.append(score)
    return scores


def natural_selection() -> None:
    global generation,best_offsprings, carry_on
    generation = 0
    best_offsprings = []
    carry_on = True

    number_of_digits = st.sidebar.slider("Number of digits", 1, 20, 6, 1, help="representing the length of DNA code")
    placeholder_seed = '5'*number_of_digits
    placeholder_target = '9'*number_of_digits
    seed = st.text_input(label="Enter the seed (%s-digit number): " %number_of_digits, value=placeholder_seed, max_chars=number_of_digits, help="Representing the DNA of the original parent")
    target = st.text_input(label="Enter the target (%s-digit number): " %number_of_digits, value=placeholder_target, max_chars=number_of_digits, help="Representing the 'DNA' code which best fits the current environment")
    st.button("Re-run")

    average_number_of_offsprings = st.sidebar.slider("Number of offsprings on average", 1.0, 2.0, 1.2, 0.1, help="Offspring rate per parent is randomly drawn from a poisson distribution with the selected rate")
    number_of_parents = st.sidebar.slider("Number of parents", 0, 1000, 200, 10, help="Amount of parents selected for every generation")
    mutation_rate_offspring = st.sidebar.slider("Chance for mutation in an offspring", 0.0, 1.0, 0.05, 0.01, help="Offspring chance to have any mutation") 
    mutation_rate_digit = st.sidebar.slider("Chance for mutation in a digit", 0.0, 1.0, 0.1, 0.05, help="For an offspring who got the chance for a mutation, this is the chance for a mutation to occur in each of the digits in the offsprings' 'DNA code'.")
    mutation_rate_digit_up = st.sidebar.slider("Chance for mutated digit to go up (versus down)", 0.0, 1.0, 0.5, 0.05, help="If a digit got a chance to mutate, this is the chance to move up or down")
    mutation_rate_digit_up_plus = st.sidebar.slider("Chance for mutated digit to jump 1 step up (versus 2 steps up)", 0.0, 1.0, 1.0, 0.05, help="For a digit which got a chance to mutate up, this is the chance to move one digit up over two digits up")
    mutation_rate_digit_down_minus = st.sidebar.slider("Chance for mutated digit to jump 1 step down (versus 2 steps down)", 0.0, 1.0, 1.0, 0.05, help="For a digit which got a chance to mutate down, this is the chance to move one digit down over two digits down")

    if len(seed) != number_of_digits or not seed.isdigit():
        st.error("Invalid seed number. Please enter a %s-digit number." %number_of_digits)

    if len(target) != number_of_digits or not target.isdigit():
        st.error("Invalid target number. Please enter a %s-digit number." %number_of_digits)

    all_offspring = []
    initial_seed = seed
    initial_score = sum(abs(int(digit1) - int(digit2)) for digit1, digit2 in zip(seed, target))
    offspring = []
    for i in range(number_of_parents):
        number_of_offsprings = np.random.poisson(average_number_of_offsprings)
        offspring.extend(generate_offspring(seed, mutation_rate_offspring, mutation_rate_digit, mutation_rate_digit_up, mutation_rate_digit_up_plus, mutation_rate_digit_down_minus, number_of_offsprings))
    scores = calculate_score(offspring, target)
    scores_sorted = scores.copy()
    scores_sorted.sort(reverse=False)
    min_scores = scores_sorted[:number_of_parents]
    best_offsprings = []
    for score in min_scores:
        best_offsprings.append(offspring[scores.index(score)])
    
    # Visualization           
    fig = plt.figure()
    X = np.random.uniform(0,1,(len(offspring)))
    Y = np.random.uniform(0,1,(len(offspring)))
    scat = plt.scatter(X,Y, c=scores, vmax=initial_score, vmin=0)
    cbar = plt.colorbar()
    cbar.set_label('Distance from %s' %target)
    text_1 = 'Generation: %s, Best offspring: %s, Distance: %s \n' %(generation, best_offsprings[0], min_scores[0])
    plt.title(text_1, fontsize = 11)
    generation += 1
    all_offspring.append(offspring)

    def gen():
        global carry_on
        i = 0
        while carry_on:
            i += 1
            yield i
        
    def update(frame_number):
        global generation,best_offsprings, carry_on

        offspring = []
        for parent in best_offsprings:
            number_of_offsprings = np.random.poisson(average_number_of_offsprings)
            offspring.extend(generate_offspring(parent, mutation_rate_offspring, mutation_rate_digit, mutation_rate_digit_up, mutation_rate_digit_up_plus, mutation_rate_digit_down_minus, number_of_offsprings))
        scores = calculate_score(offspring, target)
        scores_sorted = scores.copy()
        scores_sorted.sort(reverse=False)
        min_scores = scores_sorted[:number_of_parents]
        best_offsprings = []
        for score in min_scores:
            best_offsprings.append(offspring[scores.index(score)])

        # Visualization           
        X = np.random.uniform(0,1,(len(offspring)))
        Y = np.random.uniform(0,1,(len(offspring)))
        scat.set_offsets(np.c_[X, Y])
        scat.set_array(scores)
        text_1 = 'Generation: %s, Best offspring: %s, Distance: %s \n' %(generation, best_offsprings[0], min_scores[0])
        plt.title(text_1, fontsize = 11)
        plt.axis('off')
        generation += 1
        all_offspring.append(offspring)

        if min_scores[0] == 0:
            carry_on = False
            print("\nTarget reached!")


        return scat,

    rcParams['animation.embed_limit'] = 2**128
    with st.spinner(text="Preparing simulation..."):
        ani = FuncAnimation(fig, update, 
                    frames=gen, save_count=None, interval=100, repeat=False) 
        animjs = ani.to_jshtml()
        click_on_play = """document.querySelector('.anim-buttons button[title="Play"]').click();"""
        pattern = re.compile(r"(setTimeout.*?;)(.*?})", re.MULTILINE | re.DOTALL)
        new_animjs = pattern.sub(rf"\1 \n {click_on_play} \2", animjs)

    st.components.v1.html(new_animjs,height=600)

st.set_page_config(page_title="Natural Selection", page_icon=':earth_americas:')
st.markdown("# Natural Selection")
st.sidebar.header("Parameters")
st.sidebar.write("Change any of the following parameters to generate a new simulation")
st.write(
    """This page demonstrates the natural selection process, starting from a seed number (representing the origin parent DNA) ending at target number (representing the DNA which fits best to the environment)."""
)
with st.expander("Learn more"):
    st.write("""
        The 'DNA code' is represented by a string of digits, where every digit represents a gene. 
             Every 'gene' may have 10 variations represented by the digits 0-9. 
             A random process generates mutations in every generation.
             Mutation in every 'gene' may change it slightly so that a digit can mutate up to +-2 digits at most in every generation. 
         The offsprings which have a 'DNA' number closest to the target 'DNA' are selected as parents for the next generation.
        
    Changing the parameters, seed and target numbers will automatically generate a new simulation.
             You can also click the Re-run button to generate a new simulation using the same parameters to observe a different random process.
    """)


natural_selection()
