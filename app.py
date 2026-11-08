
import streamlit as st

import struct

def convert_ieee754(number):
    # Convert to IEEE 754 single precision
    packed = struct.pack(">f", number)
    bits = struct.unpack(">I", packed)[0]

    binary = format(bits, "032b")
    hexadecimal = format(bits, "08X")

    sign = binary[0]
    exponent = binary[1:9]
    mantissa = binary[9:]

    # Identify number classification
    exponent_value = int(exponent, 2)
    mantissa_value = int(mantissa, 2)

    if exponent_value == 255:
        if mantissa_value == 0:
            classification = "Infinity"
        else:
            classification = "NaN"
    elif exponent_value == 0:
        if mantissa_value == 0:
            classification = "Zero"
        else:
            classification = "Denormalized"
    else:
        classification = "Normalized"

    return {
        "Decimal": struct.unpack(">f", packed)[0],
        "Binary": binary,
        "Hexadecimal": hexadecimal,
        "Sign": sign,
        "Exponent": exponent,
        "Mantissa": mantissa,
        "Classification": classification
    }

def convert_from_bits(bits):
    # Decode a 32-bit IEEE 754 bit pattern
    packed = struct.pack(">I", bits)
    decimal = struct.unpack(">f", packed)[0]

    binary = format(bits, "032b")
    hexadecimal = format(bits, "08X")

    sign = binary[0]
    exponent = binary[1:9]
    mantissa = binary[9:]

    exponent_value = int(exponent, 2)
    mantissa_value = int(mantissa, 2)

    if exponent_value == 255:
        classification = (
            "Infinity" if mantissa_value == 0 else "NaN"
        )
    elif exponent_value == 0:
        classification = (
            "Zero" if mantissa_value == 0 else "Denormalized"
        )
    else:
        classification = "Normalized"

    return {
        "Decimal": decimal,
        "Binary": binary,
        "Hexadecimal": hexadecimal,
        "Sign": sign,
        "Exponent": exponent,
        "Mantissa": mantissa,
        "Classification": classification
    }

def get_number_input(label, key):
    st.subheader(label)

    input_format = st.selectbox(
        "Choose Input Format",
        ["Decimal", "Binary", "Hexadecimal",
         "Sign / Exponent / Mantissa"],
        key=f"{key}_format"
    )

    if input_format == "Decimal":
        number = st.number_input(
            "Enter decimal number",
            value=0.0,
            key=f"{key}_decimal"
        )
        return convert_ieee754(number)["Decimal"]

    elif input_format == "Binary":
        binary = st.text_input(
            "Enter 32-bit binary",
            value="00000000000000000000000000000000",
            key=f"{key}_binary"
        ).strip()

        if len(binary) != 32 or any(c not in "01" for c in binary):
            raise ValueError("Binary input must contain exactly 32 bits.")

        return convert_from_bits(int(binary, 2))["Decimal"]

    elif input_format == "Hexadecimal":
        hexadecimal = st.text_input(
            "Enter 8-digit hexadecimal",
            value="00000000",
            key=f"{key}_hex"
        ).strip()

        if len(hexadecimal) != 8:
            raise ValueError("Hexadecimal input must contain 8 digits.")

        return convert_from_bits(int(hexadecimal, 16))["Decimal"]

    else:
        sign = st.text_input(
            "Sign (1 bit)", value="0",
            key=f"{key}_sign"
        ).strip()

        exponent = st.text_input(
            "Exponent (8 bits)", value="00000000",
            key=f"{key}_exponent"
        ).strip()

        mantissa = st.text_input(
            "Mantissa (23 bits)",
            value="00000000000000000000000",
            key=f"{key}_mantissa"
        ).strip()

        combined = sign + exponent + mantissa

        if (len(sign) != 1 or len(exponent) != 8
                or len(mantissa) != 23
                or any(c not in "01" for c in combined)):
            raise ValueError("Invalid Sign, Exponent, or Mantissa.")

        return convert_from_bits(int(combined, 2))["Decimal"]

st.set_page_config(
    page_title="IEEE 754 Converter",
    page_icon="🧮",
    layout="centered"
)

st.title("IEEE 754 Floating-Point Converter")
st.write("Convert numbers and perform IEEE 754 calculations.")

converter_tab, calculator_tab, tester_tab, help_tab = st.tabs([
    "Converter",
    "Calculator",
    "Black Box Tester",
    "Help / User Guide"
])


with converter_tab:
    st.header("Number Converter")

    input_format = st.selectbox(
        "Choose Input Format",
        ["Decimal", "Binary", "Hexadecimal",
         "Sign / Exponent / Mantissa"]
    )

    if input_format == "Decimal":
        number = st.number_input(
            "Enter a decimal number", value=5.75
        )

    elif input_format == "Binary":
        binary_input = st.text_input(
            "Enter 32-bit binary",
            value="01000000101110000000000000000000"
        )

    elif input_format == "Hexadecimal":
        hex_input = st.text_input(
            "Enter 8-digit hexadecimal",
            value="40B80000"
        )

    else:
        sign_input = st.text_input(
            "Sign (1 bit)", value="0"
        )
        exponent_input = st.text_input(
            "Exponent (8 bits)", value="10000001"
        )
        mantissa_input = st.text_input(
            "Mantissa (23 bits)",
            value="01110000000000000000000"
        )

    if st.button("Convert"):
        try:
            if input_format == "Decimal":
                results = convert_ieee754(number)

            elif input_format == "Binary":
                binary_input = binary_input.strip()

                if (len(binary_input) != 32 or
                        any(c not in "01" for c in binary_input)):
                    raise ValueError(
                        "Binary must contain exactly 32 bits."
                    )

                results = convert_from_bits(
                    int(binary_input, 2)
                )

            elif input_format == "Hexadecimal":
                hex_input = hex_input.strip()

                if len(hex_input) != 8:
                    raise ValueError(
                        "Hexadecimal must contain exactly 8 digits."
                    )

                results = convert_from_bits(
                    int(hex_input, 16)
                )

            else:
                sign_input = sign_input.strip()
                exponent_input = exponent_input.strip()
                mantissa_input = mantissa_input.strip()

                combined = (
                    sign_input + exponent_input + mantissa_input
                )

                if (len(sign_input) != 1 or
                        len(exponent_input) != 8 or
                        len(mantissa_input) != 23 or
                        any(c not in "01" for c in combined)):
                    raise ValueError(
                        "Invalid Sign, Exponent, or Mantissa."
                    )

                results = convert_from_bits(
                    int(combined, 2)
                )

            st.success("Conversion Successful!")
            st.subheader("IEEE 754 Results")

            for name, value in results.items():
                st.write(f"**{name}:** {value}")

        except (ValueError, OverflowError) as error:
            st.error(f"Conversion error: {error}")



with calculator_tab:
    st.header("IEEE 754 Floating-Point Calculator")

    try:
        number1 = get_number_input("First Number", "num1")
        number2 = get_number_input("Second Number", "num2")

        operation = st.selectbox(
            "Choose Operation",
            ["Addition (+)", "Subtraction (-)", "Multiplication (*)"]
        )

        if st.button("Calculate"):
            if operation == "Addition (+)":
                result = number1 + number2
            elif operation == "Subtraction (-)":
                result = number1 - number2
            else:
                result = number1 * number2

            results = convert_ieee754(result)

            st.success("Calculation Successful!")
            st.subheader("Calculation Results")

            st.write(f"**First Number:** {number1}")
            st.write(f"**Second Number:** {number2}")

            for name, value in results.items():
                st.write(f"**{name}:** {value}")

    except (ValueError, OverflowError) as error:
        st.error(f"Input or calculation error: {error}")



with tester_tab:
    st.header("IEEE 754 Black Box Tester")

    st.write(
        "Enter the Sign, Exponent, and Mantissa "
        "to convert an IEEE 754 32-bit floating-point number."
    )

    sign = st.text_input(
        "Sign (1 bit)",
        value="0",
        key="tester_sign"
    )

    exponent = st.text_input(
        "Exponent (8 bits)",
        value="10000001",
        key="tester_exponent"
    )

    mantissa = st.text_input(
        "Mantissa (23 bits)",
        value="01110000000000000000000",
        key="tester_mantissa"
    )

    if st.button("Test Conversion"):
        try:
            sign = sign.strip()
            exponent = exponent.strip()
            mantissa = mantissa.strip()

            if (
                len(sign) != 1
                or len(exponent) != 8
                or len(mantissa) != 23
                or any(c not in "01" for c in sign + exponent + mantissa)
            ):
                raise ValueError(
                    "Enter exactly 1 sign bit, 8 exponent bits, "
                    "and 23 mantissa bits using only 0 and 1."
                )

            combined = sign + exponent + mantissa
            bits = int(combined, 2)

            results = convert_from_bits(bits)

            st.success("Conversion completed!")

            st.subheader("Floating-Point Result")
            st.metric("Decimal Value", str(results["Decimal"]))

            st.write("**Binary:**", results["Binary"])
            st.write("**Hexadecimal:**", results["Hexadecimal"])
            st.write("**Sign:**", results["Sign"])
            st.write("**Exponent:**", results["Exponent"])
            st.write("**Mantissa:**", results["Mantissa"])
            st.write(
                "**Classification:**",
                results["Classification"]
            )

        except ValueError as error:
            st.error(f"Invalid input: {error}")
with help_tab:
    st.header("IEEE 754 User Guide")

    st.write(
        "Welcome to the IEEE 754 Floating-Point "
        "Converter and Calculator!"
    )

    st.subheader("1. Number Converter")
    st.write(
        "Choose Decimal, Binary, Hexadecimal, "
        "or Sign / Exponent / Mantissa."
    )
    st.write(
        "Enter a value and click Convert to see "
        "its IEEE 754 32-bit representation."
    )

    st.subheader("2. Floating-Point Calculator")
    st.write(
        "Enter two numbers using any supported "
        "input format. Select Addition, Subtraction, "
        "or Multiplication, then click Calculate."
    )

    st.subheader("3. Black Box Tester")
    st.write(
        "Enter a 1-bit sign, 8-bit exponent, "
        "and 23-bit mantissa. Click Test Conversion "
        "to display the floating-point result."
    )

    st.subheader("4. Input Requirements")
    st.markdown("""
    - **Decimal:** Example: 5.75
    - **Binary:** Exactly 32 bits containing 0 or 1
    - **Hexadecimal:** Exactly 8 hexadecimal digits
    - **Sign:** Exactly 1 bit
    - **Exponent:** Exactly 8 bits
    - **Mantissa:** Exactly 23 bits
    """)

    st.subheader("5. Number Classifications")
    st.markdown("""
    - **Normalized:** A regular nonzero floating-point number.
    - **Denormalized:** A very small nonzero number.
    - **Zero:** Positive or negative zero.
    - **Infinity:** Positive or negative infinity.
    - **NaN:** Not a Number.
    """)

    st.subheader("6. Example")
    st.code(
        "Decimal: 5.75\n"
        "Binary: 01000000101110000000000000000000\n"
        "Hexadecimal: 40B80000\n"
        "Sign: 0\n"
        "Exponent: 10000001\n"
        "Mantissa: 01110000000000000000000"
    )

    st.info(
        "This application uses IEEE 754 "
        "32-bit single-precision floating-point numbers."
    )

