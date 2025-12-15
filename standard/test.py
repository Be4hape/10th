# import numpy as np
# import matplotlib.pyplot as plt

# t = np.linspace(-2, 4, 6001)

# u = lambda x: np.heaviside(x, 0)
# x = (u(t) - u(t-1)) + u(t-2)

# plt.plot(t, x, linewidth=2)
# plt.ylim(-0.05, 1.05)
# plt.xlim(-2.2, 4.2)
# plt.grid(True)
# plt.xlabel('t(sec)')
# plt.show()


import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(-2, 4, 6001)
u = lambda x: np.heaviside(x, 0)  # u(0)=0 (원하면 0.5로 변경)

y = 1 - 2*(u(t) - u(t-2))

plt.plot(t, y, linewidth=2)
plt.ylim(-1.2, 1.2)
plt.xlim(-2.2, 4.2)
plt.grid(True)
plt.xlabel('t(sec)')
plt.show()
