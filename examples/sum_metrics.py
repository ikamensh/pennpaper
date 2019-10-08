from pennpaper import Metric, plot

m1 = Metric()
m1.add_record(1,1)
m1.add_record(5,5)

m2 = Metric()
m2.add_record(2, 3)
m2.add_record(4, 3)


m3 = m1 + m2

print(m3.data, m3.samples)

plot(m3)
plot(m3, smoothen=False, name='true')