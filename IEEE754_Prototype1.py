"""IEEE 754 Prototype 1: converter-only Streamlit demo (32-bit single precision)."""
import struct
import streamlit as st

FORMATS = ["Decimal", "Binary (32 bits)", "Hexadecimal (8 digits)", "Sign / Exponent / Mantissa"]


def decode_bits(bits):
    """Return all displays for one unsigned 32-bit IEEE 754 bit pattern."""
    if not (0 <= bits <= 0xFFFFFFFF):
        raise ValueError("The value must fit into exactly 32 bits.")
    binary = format(bits, "032b")
    exp = (bits >> 23) & 0xFF
    fraction = bits & 0x7FFFFF
    sign = (bits >> 31) & 1
    if exp == 255:
        classification = ("Negative Infinity" if sign else "Positive Infinity") if fraction == 0 else "NaN"
    elif exp == 0:
        classification = ("Negative Zero" if sign else "Positive Zero") if fraction == 0 else "Denormalized (Subnormal)"
    else:
        classification = "Normalized"
    return {
        "Decimal": struct.unpack(">f", struct.pack(">I", bits))[0],
        "Binary": binary,
        "Hexadecimal": format(bits, "08X"),
        "Sign": binary[0],
        "Exponent": binary[1:9],
        "Mantissa": binary[9:],
        "Classification": classification,
    }


def decimal_to_bits(value):
    """Encode a Python numeric value into IEEE 754 single-precision bytes."""
    return struct.unpack(">I", struct.pack(">f", value))[0]


def format_to_bits(fmt, value):
    """Validate and encode a text-format input into a 32-bit pattern."""
    value = value.strip()
    if fmt == "Binary (32 bits)":
        if len(value) != 32 or any(bit not in "01" for bit in value):
            raise ValueError("Enter exactly 32 binary digits (0 or 1).")
        return int(value, 2)
    if fmt == "Hexadecimal (8 digits)":
        if len(value) != 8 or any(c not in "0123456789abcdefABCDEF" for c in value):
            raise ValueError("Enter exactly 8 hexadecimal digits (0-9, A-F).")
        return int(value, 16)
    if len(value) != 32 or any(bit not in "01" for bit in value):
        raise ValueError("Sign, exponent, and mantissa must total 32 binary bits.")
    return int(value, 2)


st.set_page_config(page_title="IEEE 754 | Prototype 1", page_icon="🔢", layout="centered")
st.title("IEEE 754 — Prototype 1")
st.caption("Working first prototype • 32-bit floating-point conversion")
st.write("Choose a format, enter your number, then select **Convert**.")

fmt = st.selectbox("Input format", FORMATS)
if fmt == "Decimal":
    numeric_input = st.number_input("Decimal value", value=5.75)
elif fmt == "Binary (32 bits)":
    value_input = st.text_input("32-bit binary", value="01000000101110000000000000000000")
elif fmt == "Hexadecimal (8 digits)":
    value_input = st.text_input("8-digit hexadecimal", value="40B80000")
else:
    s = st.text_input("Sign (1 bit)", value="0")
    e = st.text_input("Exponent (8 bits)", value="10000001")
    m = st.text_input("Mantissa (23 bits)", value="01110000000000000000000")

if st.button("Convert", type="primary"):
    try:
        if fmt == "Decimal":
            bits = decimal_to_bits(numeric_input)
        elif fmt == "Sign / Exponent / Mantissa":
            s, e, m = s.strip(), e.strip(), m.strip()
            if len(s) != 1 or len(e) != 8 or len(m) != 23:
                raise ValueError("Enter 1 sign bit, 8 exponent bits, and 23 mantissa bits.")
            bits = format_to_bits(fmt, s + e + m)
        else:
            bits = format_to_bits(fmt, value_input)
        st.success("Conversion completed")
        st.subheader("Conversion results")
        for label, value in decode_bits(bits).items():
            st.write(f"**{label}:** `{value}`")
    except (ValueError, OverflowError) as exc:
        st.error(f"Invalid input or out-of-range decimal number: {exc}")

with st.expander("Help / what this prototype does"):
    st.write("This version focuses on format conversion, number classification, and invalid-input checks.")
    st.write("Try decimal 5.75; the matching 32-bit hexadecimal value is **40B80000**.")
    st.write("Prototype 2 adds a two-number calculator and a dedicated Sign/Exponent/Mantissa tester.")
