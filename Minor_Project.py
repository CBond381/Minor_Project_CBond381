import streamlit as st
import pycba as cba
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

st.title("Two Span Bridge")

st.header("Dead Loads")

Dead_Load1 =st.number_input("Dead Load on Span 1 (kN/m)", 0,None,0)
Dead_Load2 =st.number_input("Dead Load on Span 2 (kN/m)", 0,None,0)


#Span1
st.sidebar.subheader('Span 1')
Span1_L = st.sidebar.number_input("Span 1 Lenth (m)",1)  
Span_1_E = st.sidebar.number_input("Span 1 E (MPa)",1)
Span_1_Ix = st.sidebar.number_input("Span 1 Ix (mm4)",1)

#Span2
st.sidebar.subheader('Span 2')
Span2_L = st.sidebar.number_input("Span 2 Length (m)",1) 
Span_2_E = st.sidebar.number_input("Span 2 E (MPa)",1)
Span_2_Ix = st.sidebar.number_input("Span 2 Ix (mm4)",1)

EI_1 = Span_1_E*Span_1_Ix #Nmm2
EI_2 = Span_2_E*Span_2_Ix #Nmm2

spans = [Span1_L, Span2_L]
EI = [EI_1, EI_2] #Nmm2
supports = [-1, 0,-1, 0, -1, 0] #Deflection and Rotation for each support
load_dl = [
    [1, 1 , Dead_Load1, 0, 0],
    [2, 1, Dead_Load2, 0, 0],
] # Span No., Load Type, Value, Distance a, Load Cover c
element_types = [1, 1]

beam_model = cba.BeamAnalysis(spans, EI, supports, load_dl, element_types)
beam_model.analyze()
x_values_DL = beam_model.beam_results.results.x
M_values_DL = beam_model.beam_results.results.M
V_values_DL = beam_model.beam_results.results.V


fig, (ax1,ax2) = plt.subplots(1,2,sharex=False, sharey=False)
ax1.plot(x_values_DL, M_values_DL)
ax1.set_title('Dead Load Moment')
ax2.set_title('Dead Load Shear')
ax2.plot(x_values_DL, V_values_DL)
st.pyplot(fig)

st.header("Live Loads")

st.subheader("Moment and Shear when truck at:")

x_loc = st.slider('Truck Location', label_visibility='hidden')
st.write("Truck front axle is at",x_loc,"m from left edge.")            
                

axle_spacings_1 = [3.6,1.2,6.6,6.6]
axle_loads_1 = [50,140,140,175,120]
CHBDC_ON_Truck = cba.Vehicle(axle_spacings=axle_spacings_1, axle_weights=axle_loads_1)

bridge_model_LL = cba.BridgeAnalysis(ba=beam_model, veh=CHBDC_ON_Truck)

static_LL_results = bridge_model_LL.static_vehicle(pos=x_loc,plotflag=True)
x_value_LL1 = static_LL_results.results.x
M_value_LL1 = static_LL_results.results.M
V_value_LL1 = static_LL_results.results.V

fig_LL1_M, ax5 = plt.subplots()
ax5.plot(x_value_LL1,M_value_LL1)
ax5.set_title("Live Load Moment for Truck at x.")
st.pyplot(fig_LL1_M)

fig_LL1_V, ax6 = plt.subplots()
ax6.plot(x_value_LL1,V_value_LL1)
ax6.set_title('Live Load Shear for Truck at x.')
st.pyplot(fig_LL1_V)


st.subheader("CL-625-ONT Truck Envelopes")

envelopes = bridge_model_LL.run_vehicle(step=0.5, plot_env=True)

M_Max= envelopes.Mmax
M_Min = envelopes.Mmin

V_Max= envelopes.Vmax
V_Min = envelopes.Vmin

x_values_LL = envelopes.x


fig_LL_M, ax3 = plt.subplots()
ax3.plot(x_values_LL,M_Max,x_values_LL,M_Min)
ax3.set_title('Live Load Moment Envelope')
st.pyplot(fig_LL_M)


fig_LL_V, ax4 = plt.subplots()
ax4.plot(x_values_LL,V_Max,x_values_LL,V_Min)
ax3.set_title('Live Load Shear Envelope')
st.pyplot(fig_LL_V)







           
