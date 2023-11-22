from functools import partial
from matplotlib import rcParams
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import re
import streamlit as st

def generate_offspring(seed, number_of_offsprings):
    offspring = []
    for _ in range(number_of_offsprings):
        offspring.append(seed)
    return offspring


def genetic_drift() -> None:
    global generation, carry_on, rand_parents
    generation = 0
    carry_on = True
    rand_parents = []

    number_of_parents = st.sidebar.slider("Amount of parents", 2, 1000, 100, 10, help="Amount of parents selected randomly in every generation")
    number_of_offsprings = st.sidebar.slider("Offsprings per parent", 1, 1000, 5, 1, help="Amount of offsprings per parent in each generation")
    number_of_generations = st.sidebar.slider("Maximum generations", 10, 5000, 500, 10, help="Stop simulation after this amount of generations, unless there is a fixation")

    placeholder_reds = int(number_of_parents/2)
    red_rate = st.number_input(label="Enter the amount of red items out of %s initial parents: " %number_of_parents, min_value=1, max_value=number_of_parents, value=placeholder_reds, help="Defines the initial distribution of red and blue items")
    blue_rate = number_of_parents - red_rate
    st.button("Re-run")

    seed_red = 'r'
    seed_blue = 'b'
    all_offspring = []
    offspring = []
    for i in range(red_rate):
        rand_parents.append(seed_red)
    for i in range(blue_rate):
        rand_parents.append(seed_blue)
    
    # Visualization     
    fig, (axl, axr) = plt.subplots(
    ncols=2,
    sharey=False,
    gridspec_kw=dict(width_ratios=[5, 1], wspace=0.5),
    )      
    axl.yaxis.set_visible(False)
    axl.xaxis.set_visible(False)
    X = np.random.uniform(0,1,(number_of_parents))
    Y = np.random.uniform(0,1,(number_of_parents))
    scat = axl.scatter(X,Y, c=rand_parents)
    text_1 = 'Generation: %s' %generation
    axl.title.set_text(text_1)
    axl.axis('off')

    pops = ['red', 'blue']
    counts = [red_rate, blue_rate]
    bar_labels = ['red', 'blue']
    bar_colors = ['tab:red', 'tab:blue']

    bar_pop = axr.bar(pops, counts, label=bar_labels, color=bar_colors)
    axr.set_ylabel('Population distribution')
    axr.set_ylim([0, number_of_parents*number_of_offsprings])
    axr.spines[['right', 'top']].set_visible(False)

    generation += 1

    def gen():
        global carry_on
        i = 0
        while carry_on:
            i += 1
            yield i
        
    def update(frame_number):
        global generation, carry_on, rand_parents

        offspring = []
        for parent in rand_parents:
            offspring.extend(generate_offspring(parent, number_of_offsprings))

        red_rate = offspring.count(seed_red)
        blue_rate = offspring.count(seed_blue)
        rand_parents = random.sample(offspring, number_of_parents)

        # Visualization           
        X = np.random.uniform(0,1,(number_of_offsprings*number_of_parents))
        Y = np.random.uniform(0,1,(number_of_offsprings*number_of_parents))
        scat.set_offsets(np.c_[X, Y])
        scat.set_facecolors(rand_parents)
        text_1 = 'Generation: %s' %generation
        axl.title.set_text(text_1)
        axl.axis('off')

        pops = ['red', 'blue']
        counts = [red_rate, blue_rate]
        bar_labels = ['red', 'blue']
        bar_colors = ['tab:red', 'tab:blue']
        for i in range(len(bar_pop)):
            bar_pop[i].set_height(counts[i])

        all_offspring.append(offspring)

        if generation >= number_of_generations or len(set(offspring)) == 1:
            carry_on = False
            print("\nStopping at generation %s!" %generation)

        generation += 1        


        return scat, bar_pop,

    rcParams['animation.embed_limit'] = 2**128
    with st.spinner(text="Preparing simulation..."):
        ani = FuncAnimation(fig, update, 
                    frames=gen, save_count=None, interval=100, repeat=False) 
        animjs = ani.to_jshtml()
        click_on_play = """document.querySelector('.anim-buttons button[title="Play"]').click();"""
        pattern = re.compile(r"(setTimeout.*?;)(.*?})", re.MULTILINE | re.DOTALL)
        new_animjs = pattern.sub(rf"\1 \n {click_on_play} \2", animjs)

    st.components.v1.html(new_animjs,height=600)

st.set_page_config(page_title="Genetic Drift", page_icon=':earth_americas:')
st.markdown("# Genetic Drift")
st.sidebar.header("Parameters")
st.sidebar.write("Change any of the following parameters to generate a new simulation")
st.write(
    """This simulation demonstrates the genetic drift process, starting with two populations 
    of specified distribution. In each generation parents are randomly selected to create 
    the next generation. Fixation is reached when one population dominates and the other is extincted."""
)
with st.expander("Learn more"):
    st.write("""
        The process of genetic drift occurs normally in small populations, 
             in which there is a genetic variaty between the groups 
             (here represented by red and blue populations). 
             A random process selects just a few parents every generation 
             without any advatage for any of the groups 
             (representing natural processes such as the founder effect). 
             A fixation of a specific gene is possible as 
             demonstrated in the simulation, when one population is extincted. 

        For simplicity, the model assumes that there is a single gene 
             with only two variations (red and blue), and that there are no mutations.
                     
        Changing the parameters will automatically generate a new simulation.
             You can also click the Re-run button to generate a new simulation using 
             the same parameters to observe a different random process with a different outcome.
    """)


genetic_drift()
