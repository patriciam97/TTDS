import subprocess

def get_correct():
  cmd = "./svm_multiclass_classify ./data/results/feats.test model temp.out"
  test = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
  output = test.communicate()[0]
  output = output.decode().split()
  correct = output[-6][1:]
  return correct

def train(c):
  cmd = "./svm_multiclass_learn -c {} ./data/results/feats.train model".format(c)
  test = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
  output = test.communicate()
  test.wait()

f = open("graph.txt", "w")
for c in range(1000, 10001, 250):
  train(c)
  val = get_correct()
  print(c, val)
  f.write("{}:{}".format(c, val))
  f.write("\n")
f.close()
