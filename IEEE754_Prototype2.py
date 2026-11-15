"""IEEE 754 Prototype 2: conversion + calculator + black-box tester."""
import struct
import streamlit as st

FORMATS = ["Decimal", "Binary (32 bits)", "Hexadecimal (8 digits)", "Sign / Exponent / Mantissa"]


def decode_bits(bits):
    """Decode an unsigned 32-bit pattern into IEEE 754 displays."""
    if not 0 <= bits <= 0xFFFFFFFF:
        raise ValueError("Bit pattern must be in the 32-bit range.")
    binary = format(bits, "032b")
    sign = (bits >> 31) & 1
    exponent = (bits >> 23) & 255
    mantissa = bits & 0x7FFFFF
    if exponent == 255:
        kind = ("Negative Infinity" if sign else "Positive Infinity") if mantissa == 0 else "NaN"
    elif exponent == 0:
        kind = ("Negative Zero" if sign else "Positive Zero") if mantissa == 0 else "Denormalized (Subnormal)"
    else:
        kind = "Normalized"
    return {
        "Decimal": struct.unpack(">f", struct.pack(">I", bits))[0],
        "Binary": binary,
        "Hexadecimal": format(bits, "08X"),
        "Sign": binary[0],
        "Exponent": binary[1:9],
        "Mantissa": binary[9:],
        "Classification": kind,
    }


def decimal_to_bits(number):
    return struct.unpack(">I", struct.pack(">f", number))[0]


def parse_pattern(fmt, text):
    text = text.strip()
    if fmt == "Binary (32 bits)" or fmt == "Sign / Exponent / Mantissa":
        if len(text) != 32 or any(c not in "01" for c in text):
            raise ValueError("Binary input must contain exactly 32 zeros or ones.")
        return int(text, 2)
    if fmt == "Hexadecimal (8 digits)":
        if len(text) != 8 or any(c not in "0123456789abcdefABCDEF" for c in text):
            raise ValueError("Hexadecimal input must contain exactly 8 digits (0-9, A-F).")
        return int(text, 16)
    raise ValueError("Unsupported input format.")


def input_bits(label, key, initial=5.75):
    """Draw input widgets and return a bit pattern for the selected input."""
    st.markdown(f"**{label}**")
    fmt = st.selectbox(f"{label} format", FORMATS, key=f"{key}_fmt")
    if fmt == "Decimal":
        return decimal_to_bits(st.number_input(f"{label} decimal", value=float(initial), key=f"{key}_decimal"))
    if fmt == "Binary (32 bits)":
        text = st.text_input(f"{label} binary", value="01000000101110000000000000000000", key=f"{key}_binary")
    elif fmt == "Hexadecimal (8 digits)":
        text = st.text_input(f"{label} hexadecimal", value="40B80000", key=f"{key}_hex")
    else:
        s = st.text_input(f"{label} sign (1 bit)", value="0", key=f"{key}_sign").strip()
        e = st.text_input(f"{label} exponent (8 bits)", value="10000001", key=f"{key}_exp").strip()
        m = st.text_input(f"{label} mantissa (23 bits)", value="01110000000000000000000", key=f"{key}_mant").strip()
        if len(s) != 1 or len(e) != 8 or len(m) != 23:
            raise ValueError("Use 1 sign bit, 8 exponent bits, and 23 mantissa bits.")
        text = s + e + m
    return parse_pattern(fmt, text)


def display_result(bits):
    for label, value in decode_bits(bits).items():
        st.write(f"**{label}:** `{value}`")


st.set_page_config(page_title="IEEE 754 | Prototype 2", page_icon="🧮", layout="centered")
st.title("IEEE 754 — Prototype 2")
st.caption("Expanded prototype • Converter + Calculator + Black Box Tester")
converter_tab, calculator_tab, tester_tab, help_tab = st.tabs([
    "Converter", "Calculator", "Black Box Tester", "Help"
])

with converter_tab:
    st.header("Number converter")
    try:
        bits = input_bits("Input", "converter")
        if st.button("Convert", type="primary"):
            st.success("Conversion completed")
            display_result(bits)
    except (ValueError, OverflowError) as exc:
        st.error(f"Invalid input or number too large: {exc}")

with calculator_tab:
    st.header("Floating-point calculator")
    st.write("Enter two numbers using any supported format, then choose an operation.")
    try:
        bits_a = input_bits("First number", "left", 5.0)
        bits_b = input_bits("Second number", "right", 3.0)
        operation = st.selectbox("Operation", ["Addition (+)", "Subtraction (-)", "Multiplication (*)"])
        if st.button("Calculate", type="primary"):
            a = decode_bits(bits_a)["Decimal"]
            b = decode_bits(bits_b)["Decimal"]
            if operation == "Addition (+)":
                result = a + b
            elif operation == "Subtraction (-)":
                result = a - b
            else:
                result = a * b
            result_bits = decimal_to_bits(result)
            st.write(f"**Operands:** {a} and {b}")
            st.success("Calculation completed")
            display_result(result_bits)
    except (ValueError, OverflowError) as exc:
        st.error(f"Input or calculation error: {exc}")

with tester_tab:
    st.header("Black Box Tester")
    st.write("Enter Sign, Exponent, and Mantissa to test a 32-bit IEEE 754 conversion.")
    sign = st.text_input("Sign (1 bit)", value="0", key="tester_s")
    exponent = st.text_input("Exponent (8 bits)", value="10000001", key="tester_e")
    mantissa = st.text_input("Mantissa (23 bits)", value="01110000000000000000000", key="tester_m")
    if st.button("Test Conversion", type="primary"):
        try:
            s, e, m = sign.strip(), exponent.strip(), mantissa.strip()
            if len(s) != 1 or len(e) != 8 or len(m) != 23:
                raise ValueError("Enter exactly 1 sign bit, 8 exponent bits, and 23 mantissa bits.")
            bits = parse_pattern("Sign / Exponent / Mantissa", s + e + m)
            st.success("Tester conversion completed")
            st.metric("Decimal value", str(decode_bits(bits)["Decimal"]))
            display_result(bits)
        except ValueError as exc:
            st.error(f"Invalid tester input: {exc}")

with help_tab:
    st.header("How to use this prototype")
    st.write("**Converter:** Choose one of four formats and select Convert.")
    st.write("**Calculator:** Enter two numbers and select +, -, or ×.")
    st.write("**Black Box Tester:** Enter 1 sign bit, 8 exponent bits, and 23 mantissa bits.")
    st.info("IEEE 754 single precision (32-bit). Very large results may show an overflow error in this prototype.")
