import marimo

__generated_with = "0.21.1"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(rf"""
    # Protocolo I²C

    ## Objetivos de aprendizado

    Neste notebook, você vai:

    1. **Compreender o propósito do protocolo**:
        1.1 O que é I²C?
        1.2 Porque surgiu?
        1.3 Quais problemas resolve?

    2. **Entender os fundamentos**:
        2.1 Linhas de barramento: SDA e SCL;
        2.2 Papeis no barramento: Controlador e dispositivos;
        2.3 Eventos especiais: idle, START e STOP;
        2.4 Estrutura do quadro: Endereço, bit R/W, ACK, dados.

    4. **Implementar e visualizar um quadro I²C**
        3.1 Construção do tempo discreto;
        3.2 Geração de sinais SDA e SCL;
        3.3 Modelagem de START, bits, ACK e STOP;
        3.4 Plot das formas de onda;
        3.5 Leitura técnica do quadro gerado;
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ---
    ## Parte 1: Compreender o propósito do protocolo

    ### 1.1 O que é I²C?
    [span_0](start_span)[span_1](start_span)O I²C (**Inter-Integrated Circuit**) é um sistema de barramento de dois fios, consistindo em uma linha de **clock** (SCL) e uma linha de **dados** (SDA)[span_0](end_span)[span_1](end_span). [span_2](start_span)Ele foi projetado para interconectar diversas "estações", como microcomputadores, memórias, sensores e dispositivos de E/S[span_2](end_span).

    ### 1.2 Por que surgiu?
    [span_3](start_span)O protocolo surgiu da necessidade de permitir que uma única linha de dois fios interconectasse um número ilimitado de estações de forma confiável[span_3](end_span). [span_4](start_span)Antes dele, sistemas comuns transportavam dados em apenas uma direção ou exigiam barramentos paralelos complexos[span_4](end_span).

    ### 1.3 Quais problemas resolve?
    * **[span_5](start_span)Redução de fiação:** Substitui barramentos complexos por apenas dois fios[span_5](end_span).
    * **[span_6](start_span)[span_7](start_span)Conflitos de barramento:** Resolve disputas através de um mecanismo de **arbitragem**, permitindo que múltiplos mestres tentem usar o barramento simultaneamente sem corromper os dados[span_6](end_span)[span_7](end_span).
    * **[span_8](start_span)[span_9](start_span)Sincronização:** Permite que dispositivos com velocidades diferentes (frequências de clock distintas) se comuniquem, pois o clock é controlado pelo mestre e sincronizado entre as estações[span_8](end_span)[span_9](end_span).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ---
    ## Parte 2: Entender os fundamentos

    
    ### 2.1 Linhas de barramento: SDA e SCL
    [span_10](start_span)[span_11](start_span)O barramento I²C utiliza uma lógica de **"AND cabeado"** (wired-AND)[span_10](end_span)[span_11](end_span).
    * **[span_12](start_span)SCL (Serial Clock):** Transporta o sinal de sincronização[span_12](end_span).
    * **[span_13](start_span)SDA (Serial Data):** Transporta os bits de dados[span_13](end_span).
    * **[span_14](start_span)[span_15](start_span)Pull-up Resistors:** Ambos os fios são conectados a uma tensão positiva ($V_{DD}$) através de resistores, que mantêm a linha em nível **ALTO** na ausência de sinal[span_14](end_span)[span_15](end_span).

    ### 2.2 Papéis no barramento
    * **[span_16](start_span)[span_17](start_span)Mestre (Master):** A estação que inicia a transferência, gera o sinal de clock e termina a comunicação[span_16](end_span)[span_17](end_span).
    * **[span_18](start_span)Escravo (Slave):** A estação que é endereçada e controlada pelo mestre[span_18](end_span).
    * **[span_19](start_span)[span_20](start_span)Transmissor vs Receptor:** Uma estação pode mudar de papel; por exemplo, um mestre pode enviar dados (transmissor) e depois aguardar uma resposta de um escravo (receptor)[span_19](end_span)[span_20](end_span).

    ### 2.3 Eventos especiais: Idle, START e STOP
    [span_21](start_span)A detecção desses estados é fundamental para que as estações saibam quando o barramento está livre ou ocupado[span_21](end_span).
    * **[span_22](start_span)[span_23](start_span)Idle (Livre):** Ambas as linhas (SDA e SCL) permanecem em nível **ALTO**[span_22](end_span)[span_23](end_span).
    * **[span_24](start_span)[span_25](start_span)START:** Ocorre quando a linha SDA passa de **ALTO para BAIXO** enquanto a linha SCL está em **ALTO**[span_24](end_span)[span_25](end_span).
    * **[span_26](start_span)[span_27](start_span)STOP:** Ocorre quando a linha SDA passa de **BAIXO para ALTO** enquanto a linha SCL está em **ALTO**[span_26](end_span)[span_27](end_span).

    
    ### 2.4 Estrutura do quadro
    [span_28](start_span)Os dados são enviados em pacotes de **8 bits** (1 byte)[span_28](end_span).
    * **[span_29](start_span)Endereço:** Geralmente possui **7 bits**, permitindo identificar qual escravo deve responder[span_29](end_span).
    * **[span_30](start_span)Bit R/W:** Define se a operação é de escrita (0) ou leitura (1)[span_30](end_span).
    * **[span_31](start_span)ACK (Acknowledge):** Após cada byte, o receptor deve enviar um 9º bit puxando a linha SDA para **BAIXO** para confirmar o recebimento[span_31](end_span).
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
    addr_bits = [0, 1, 1, 1, 0, 1, 0]  # example 7-bit address (MSB first)
    rw_bit = [0]  # write
    data_bits = [1, 0, 1, 0, 0, 1, 1, 0]  # example data byte (MSB first)

    # Count slots: one slot per data bit, plus two ACK slots (after address and after data)
    num_bits = len(addr_bits) + len(rw_bit) + len(data_bits)
    ack_slots = 2
    pulse_count = num_bits + ack_slots  # total clock pulses (one per bit/ack)

    # Generate pulse time edges (slot boundaries)
    pulse_times = np.linspace(
        clk_start, clk_end, pulse_count + 1
    )  # edges for each slot
    slot_edges = pulse_times[:-1]  # start times for each slot
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
    ack1_idx = len(addr_bits) + len(rw_bit)  # index of first ACK slot
    ack2_idx = ack1_idx + len(data_bits)  # index of second ACK slot

    # Drive ACKs low (receiver pulls SDA low during ACK clock)
    sda[(t >= slot_edges[ack1_idx]) & (t < slot_edges[ack1_idx] + bit_duration)] = (
        0.0
    )
    sda[(t >= slot_edges[ack2_idx]) & (t < slot_edges[ack2_idx] + bit_duration)] = (
        0.0
    )

    # STOP condition: SDA rises while SCL is HIGH (after clocks)
    sda[t >= 8.0] = 1.0


    # Convert to sharp steps for plotting
    def step(y):
        return np.where(y > 0.5, 1.0, 0.0)


    sclp = step(scl)
    sdap = step(sda)

    # Plot
    plt.figure(figsize=(10, 3.5))
    plt.plot(t, sclp * 0.9 + 0.1, label="SCL", color="tab:blue")
    plt.plot(t, sdap * 0.4 - 0.1, label="SDA", color="tab:orange")
    plt.ylim(-0.3, 1.05)
    plt.yticks([])
    plt.xlabel("time (arb. units)")
    plt.title("I2C single-frame waveform (Start, Addr+R/W, ACK, Data, ACK, Stop)")

    # Annotations
    plt.annotate(
        "Idle (HIGH)",
        xy=(1.0, 0.95),
        xytext=(0.8, 1.02),
        arrowprops=dict(arrowstyle="->"),
    )
    plt.annotate(
        "START (SDA FALL while SCL HIGH)",
        xy=(1.8, 0.6),
        xytext=(2.4, 0.9),
        arrowprops=dict(arrowstyle="->"),
    )
    plt.annotate(
        "Address bits (MSB→LSB)",
        xy=(3.0, 0.6),
        xytext=(4.0, 0.95),
        arrowprops=dict(arrowstyle="->"),
    )
    plt.annotate(
        "ACK (SDA LOW during ACK clock)",
        xy=(5.0, -0.05),
        xytext=(5.3, -0.25),
        arrowprops=dict(arrowstyle="->"),
    )
    plt.annotate(
        "Data bits",
        xy=(5.6, 0.6),
        xytext=(6.4, 0.95),
        arrowprops=dict(arrowstyle="->"),
    )
    plt.annotate(
        "STOP (SDA RISE while SCL HIGH)",
        xy=(8.2, 0.6),
        xytext=(8.8, 0.95),
        arrowprops=dict(arrowstyle="->"),
    )

    # Vertical lines at clock edges where data is sampled
    for pt in pulse_times[1:]:
        plt.axvline(pt, color="gray", alpha=0.2, linewidth=0.8)

    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
