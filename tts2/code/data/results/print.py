with open("./Eval2.txt", "r") as f:
    for i, line in enumerate(f.readlines()[3:], 1):
        print(" & ".join([str(i)]+list(map(lambda x: x.split("=")[
              1], line.strip().split(" ")[1:])))+" \\\\")
        print("\hline")