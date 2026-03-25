import marimo

__generated_with = "0.21.1"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Protocolo I²C

    ## Objetivos de aprendizado

    Neste notebook, você vai:

    1. **Compreender o propósito do protocolo**:
      1.1 O que é I²C?
      1.2 Porque surgiu?
      1.3 Qual problema resolve?

    2. **Entender os fundamentos**:
      2.1 Linhas de barramento: SDA e SCL;
      2.2 Papeis no barramento: Controlador e dispositivos;
      2.3 Eventos especiais: idle, START e STOP;
      2.4 Estrutura do quadro: Endereço, bit R/W, ACK, dados.

    3. **Implementar e visualizar um quadro I²C**
      3.1 Construção do tempo discreto;
      3.2 Geração de sinais SDA e SCL;
      3.3 Modelagem de START, bits, ACK e STOP;
      3.4 Plot das formas de onda;
      3.5 Leitura técnica do quadro gerado;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Parte 1: Compreender o propósito do protocolo
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Parte 2: Entender os fundamentos
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Parte 3: Implementar e visualizar um quadro I²C
    """)
    return


@app.cell
def _():
    # célula 1: Importações
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    print("Bibliotecas importadas com sucesso!")
    return mo, np, plt


@app.cell
def _(np, plt):
    # Time axis
    t = np.linspace(0, 10, 1000)

    # Define clock window
    clk_start, clk_end = 2.0, 7.5

    # Define bits: address(7) + R/W(1) + data(8)
    addr_bits = [0,1,1,1,0,1,0]             # example 7-bit address (MSB first)
    rw_bit = [0]                            # write
    data_bits = [1,0,1,0,0,1,1,0]           # example data byte (MSB first)

    # Count slots: one slot per data bit, plus two ACK slots (after address and after data)
    num_bits = len(addr_bits) + len(rw_bit) + len(data_bits)
    ack_slots = 2
    pulse_count = num_bits + ack_slots      # total clock pulses (one per bit/ack)

    # Generate pulse time edges (slot boundaries)
    pulse_times = np.linspace(clk_start, clk_end, pulse_count + 1)  # edges for each slot
    slot_edges = pulse_times[:-1]            # start times for each slot
    bit_duration = slot_edges[1] - slot_edges[0]

    # Build SCL: idle HIGH, square low pulses for each slot's first half
    scl = np.ones_like(t)
    for i in range(pulse_count):
        low_start = slot_edges[i]
        low_end = low_start + bit_duration * 0.5
        low_mask = (t >= low_start) & (t < low_end)
        scl[low_mask] = 0.0

    # Build SDA: idle HIGH
    sda = np.ones_like(t)

    # START condition: SDA falls while SCL is HIGH (place before clocks)
    sda[(t >= 1.6) & (t < 2.0)] = 0.0

    # Compose bit sequence (address + R/W + data)
    bits = addr_bits + rw_bit + data_bits

    # Place bits into SDA slots (data changes while SCL low; here we set per slot for clarity)
    for i, b in enumerate(bits):
        slot_start = slot_edges[i]
        slot_end = slot_start + bit_duration
        sda[(t >= slot_start) & (t < slot_end)] = b

    # ACK slots: first ACK follows address+R/W, second follows data
    ack1_idx = len(addr_bits) + len(rw_bit)             # index of first ACK slot
    ack2_idx = ack1_idx + len(data_bits)                # index of second ACK slot

    # Drive ACKs low (receiver pulls SDA low during ACK clock)
    sda[(t >= slot_edges[ack1_idx]) & (t < slot_edges[ack1_idx] + bit_duration)] = 0.0
    sda[(t >= slot_edges[ack2_idx]) & (t < slot_edges[ack2_idx] + bit_duration)] = 0.0

    # STOP condition: SDA rises while SCL is HIGH (after clocks)
    sda[t >= 8.0] = 1.0

    # Convert to sharp steps for plotting
    def step(y):
        return np.where(y > 0.5, 1.0, 0.0)

    sclp = step(scl)
    sdap = step(sda)

    # Plot
    plt.figure(figsize=(10,3.5))
    plt.plot(t, sclp*0.9 + 0.1, label='SCL', color='tab:blue')
    plt.plot(t, sdap*0.4 - 0.1, label='SDA', color='tab:orange')
    plt.ylim(-0.3,1.05)
    plt.yticks([])
    plt.xlabel('time (arb. units)')
    plt.title('I2C single-frame waveform (Start, Addr+R/W, ACK, Data, ACK, Stop)')

    # Annotations
    plt.annotate('Idle (HIGH)', xy=(1.0,0.95), xytext=(0.8,1.02), arrowprops=dict(arrowstyle='->'))
    plt.annotate('START (SDA FALL while SCL HIGH)', xy=(1.8,0.6), xytext=(2.4,0.9), arrowprops=dict(arrowstyle='->'))
    plt.annotate('Address bits (MSB→LSB)', xy=(3.0,0.6), xytext=(4.0,0.95), arrowprops=dict(arrowstyle='->'))
    plt.annotate('ACK (SDA LOW during ACK clock)', xy=(5.0, -0.05), xytext=(5.3, -0.25), arrowprops=dict(arrowstyle='->'))
    plt.annotate('Data bits', xy=(5.6,0.6), xytext=(6.4,0.95), arrowprops=dict(arrowstyle='->'))
    plt.annotate('STOP (SDA RISE while SCL HIGH)', xy=(8.2,0.6), xytext=(8.8,0.95), arrowprops=dict(arrowstyle='->'))

    # Vertical lines at clock edges where data is sampled
    for pt in pulse_times[1:]:
        plt.axvline(pt, color='gray', alpha=0.2, linewidth=0.8)

    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
