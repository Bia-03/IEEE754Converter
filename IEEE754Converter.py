
import struct

# Convert a decimal number into IEEE 754 bits
def decimal_to_bits(number):
    packed = struct.pack(">f", number)
    return struct.unpack(">I", packed)[0]


# Identify the IEEE 754 floating-point category
def classify_number(bits):
    sign = (bits >> 31) & 1
    exponent = (bits >> 23) & 0xFF
    mantissa = bits & 0x7FFFFF

    if exponent == 255:
        if mantissa == 0:
            return "Positive Infinity" if sign == 0 else "Negative Infinity"
        return "NaN (Not a Number)"

    elif exponent == 0:
        if mantissa == 0:
            return "Positive Zero" if sign == 0 else "Negative Zero"
        return "Denormalized (Subnormal)"

    else:
        return "Normalized"

# Display all IEEE 754 representations
def show_results(bits):
    binary = format(bits, "032b")
    hexadecimal = format(bits, "08X")
    decimal = struct.unpack(">f", struct.pack(">I", bits))[0]

    sign = binary[0]
    exponent = binary[1:9]
    mantissa = binary[9:]

    print("\n--- Conversion Results ---")
    print("Decimal:", decimal)
    print("Binary:", binary)
    print("Hexadecimal:", hexadecimal)
    print("Sign:", sign)
    print("Exponent:", exponent)
    print("Mantissa:", mantissa)
    print("Classification:", classify_number(bits))


# Convert user input into a 32-bit IEEE 754 pattern
def get_input_bits():
    print("\nChoose Input Format:")
    print("1. Decimal")
    print("2. Binary")
    print("3. Hexadecimal")
    print("4. Sign / Exponent / Mantissa")

    choice = input("Choose input format (1-4): ").strip()

    if choice == "1":
        number = float(input("Enter decimal number: "))
        return decimal_to_bits(number)

    elif choice == "2":
        binary = input("Enter 32-bit binary: ").strip()

        if len(binary) != 32 or any(c not in "01" for c in binary):
            raise ValueError("Binary input must contain exactly 32 bits.")

        return int(binary, 2)

    elif choice == "3":
        hexadecimal = input("Enter 8-digit hexadecimal: ").strip()

        if len(hexadecimal) != 8:
            raise ValueError("Hexadecimal input must contain exactly 8 digits.")

        return int(hexadecimal, 16)

    elif choice == "4":
        sign = input("Enter sign (1 bit): ").strip()
        exponent = input("Enter exponent (8 bits): ").strip()
        mantissa = input("Enter mantissa (23 bits): ").strip()

        combined = sign + exponent + mantissa

        if (len(sign) != 1 or len(exponent) != 8
                or len(mantissa) != 23
                or any(c not in "01" for c in combined)):
            raise ValueError("Invalid sign, exponent, or mantissa.")

        return int(combined, 2)

    else:
        raise ValueError("Invalid input format.")


def calculator():
    print("\n--- IEEE 754 Calculator ---")

    print("\nFirst number:")
    bits1 = get_input_bits()

    print("\nSecond number:")
    bits2 = get_input_bits()

    number1 = struct.unpack(">f", struct.pack(">I", bits1))[0]
    number2 = struct.unpack(">f", struct.pack(">I", bits2))[0]

    print("\nChoose Operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")

    operation = input("Choose operation (1-3): ").strip()

    if operation == "1":
        result = number1 + number2
    elif operation == "2":
        result = number1 - number2
    elif operation == "3":
        result = number1 * number2
    else:
        raise ValueError("Invalid operation.")

    result_bits = decimal_to_bits(result)

    print("\nNumber 1:", number1)
    print("Number 2:", number2)

    show_results(result_bits)


# Main program
print("IEEE 754 Floating-Point Converter and Calculator")
print("------------------------------------------------")

print("1. Convert a Number")
print("2. Calculator")

choice = input("Choose option (1-2): ").strip()

try:
    if choice == "1":
        bits = get_input_bits()
        show_results(bits)

    elif choice == "2":
        calculator()

    else:
        print("Invalid menu option.")

except (ValueError, OverflowError) as error:
    print("Error:", error)
