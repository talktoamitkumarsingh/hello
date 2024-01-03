from kite_trade import *
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


def myFunc(e):
    return e


def stop_loss(value):
    matches = ["price:"]

    value = value.replace(' ', "")
    spe_char_to_remove = ['{', '}']
    for character in spe_char_to_remove:
        value = value.replace(character, '')
    value = value.replace("'", "")
    value = value.replace("]", "")
    value = value.replace("[", "")
    l1 = value.split(",")
    flag = 0
    p_list = []
    for i in l1:

        if any(x in i for x in matches):
            if flag > 1:
                v1 = i.split(":")
                p_list.append(float(v1[-1]))
            flag = flag + 1

    p_list.sort(key=myFunc)
    print(p_list)


def create_list(r1, r2):
    return list(map(lambda x: x, range(r1, r2 + 1)))


def animate(i):
    style.use('fivethirtyeight')
    y = []
    z = []
    ax1 = fig.add_subplot(1, 1, 1)
    ax1 = plt.gca()
    ax1.set_xlim([0, 1200])
    ax1.set_ylim([17000, 28000])

    my_file = open("oi_ce_data.txt", "r")
    data = my_file.read()
    data_into_list = data.split("\n")

    data_into_list_1 = data_into_list.pop()
    for i in range(0, len(data_into_list)):
        data_into_list[i] = int(data_into_list[i])
        y.append(int(data_into_list[i]))

    r1 = 1
    r2 = (len(data_into_list))
    x = create_list(r1, r2)
    my_file.close()
    ax1.clear()
    ax1.plot(x, y, label="l1", color='green', lw=2, )

    my_file_1 = open("oi_pe_data.txt", "r")
    data = my_file_1.read()
    data_into_list_pe = data.split("\n")
    data_into_list_pe_1 = data_into_list_pe.pop()

    for i in range(0, len(data_into_list_pe)):
        data_into_list[i] = int(data_into_list_pe[i])
        z.append(int(data_into_list[i]))

    ax1.plot(x, z, label="l2", color='red', lw=2)

    plt.xlabel('Time')
    plt.ylabel('OI Value')
    plt.title('OI GRAPH')

    fig.savefig("oi.png", dpi=199)
    plt.close(fig)


def delta_adjustment(temp):
    flag_thou = 1000
    flag_hund = 100
    flag_ten = 10
    flag_one = 1

    flag_thou = int((float(temp)) / 1000)
    flag_hund = int((float(temp)) % 1000)
    flag_ten = flag_hund % 100
    flag_hund = int((float(flag_hund)) / 100)
    flag_ten = int(flag_ten / 10)
    flag_one = int(float(temp)) % 10

    #  print(flag_thou, flag_hund, flag_ten, flag_one)
    num = int(flag_ten * 10 + flag_one * 1)

    if (num >= 50):
        num = num - 50

    return num


def oi_data_file(value1: int, value2: int):
    file1 = open("oi_ce_data.txt", "a")
    file1.writelines(str(value1))
    file1.write("\n")
    file1.close()

    file2 = open("oi_pe_data.txt", "a")
    file2.writelines(str(value2))
    file2.write("\n")
    file2.close()


def range_calculation(temp) -> list:
    flag_thou = 1000
    flag_hund = 100
    flag_ten = 10
    flag_one = 1

    master_string_pe = ""
    master_string_ce = ""
    master_list = ["CE", "PE"]
    pre_string = "NFO:NIFTY24104"

    flag_thou = int((float(temp)) / 1000)
    flag_hund = int((float(temp)) % 1000)
    flag_ten = flag_hund % 100
    flag_hund = int((float(flag_hund)) / 100)
    flag_ten = int(flag_ten / 10)
    flag_one = int(float(temp)) % 10

    # print(flag_thou, flag_hund, flag_ten , flag_one)
    num = int(flag_ten * 10 + flag_one * 1)

    if (num >= 50):
        number = flag_thou * 1000 + flag_hund * 100 + 50
        number = int(float(number)) - 500

    if (num < 50):
        number = flag_thou * 1000 + flag_hund * 100 + 0
        number = int(float(number)) - 500

    for i in range(21):
        master_string = pre_string + str(number) + "CE"

        master_string_ce = master_string_ce + master_string + ","

        master_string = pre_string + str(number) + "PE"
        master_string_pe = master_string_pe + master_string + ","

        number = number + 50

    master_list[0] = master_string_ce
    master_list[1] = master_string_pe
    return master_list


def nse_current(value):
    value = value.replace(' ', "")
    spe_char_to_remove = ['{', '}']
    for character in spe_char_to_remove:
        value = value.replace(character, '')
    value = value.replace("'", "")
    l1 = value.split(":")
    return (l1[len(l1) - 1])


def oi_calculation(value) -> list:
    matches_oi = ["oi:"]
    matches_oi_day_low = ["oi_day_low:"]
    matches_oi_day_high = ["oi_day_high:"]
    instrument_name = ["NIFTY"]
    final_list = ["NIFTY", "oi", "oi_day_low", "oi_day_high"]

    value = value.replace(' ', "")
    spe_char_to_remove = ['{', '}']
    for character in spe_char_to_remove:
        value = value.replace(character, '')
    value = value.replace("'", "")
    value = value.replace("]", "")
    value = value.replace("[", "")
    l1 = value.split(",")

    for i in l1:
        if any(x in i for x in instrument_name):
            temp_str = str(i)
            temp_list = temp_str.split(":")

            temp_str = temp_list[1]
            leng = len(temp_str)
            n = 7
            final_list[0] = temp_str[leng - n:]

        if any(x in i for x in matches_oi):
            temp_str = str(i)
            temp_list = temp_str.split(":")
            final_list[3] = temp_list[1]

        if any(x in i for x in matches_oi_day_low):
            temp_str = str(i)
            temp_list = temp_str.split(":")
            final_list[2] = temp_list[1]

        if any(x in i for x in matches_oi_day_high):
            temp_str = str(i)
            temp_list = temp_str.split(":")
            final_list[1] = temp_list[1]
    return final_list


enctoken = "oBcYJpaeAHEdKDnwA++ciRgM643qGuwHLu2oBBqHGobwsUGQaBGz9MXi3A6aq6rFsMmZrumVOGkokE9E/FPzJwu0x3hDbsljAlxIEuqlCQx6lh3PWaqxNg=="


kite = KiteApp(enctoken=enctoken)
t_end = time.time() + 50 * 60
master_list = [" ", " "]
all_oi_ce = 0
all_oi_pe = 0
delta_adj = 0.00

prev_day_ce_oi = 20693
prev_day_pe_oi = 18325

while time.time() < t_end:
    s0 = str((kite.ltp('NSE:NIFTY 50')))
    current_value = nse_current(s0)
    print(current_value)
    current_value = "21650"
    delta_adj = float(delta_adjustment(current_value))

    master_list = range_calculation(current_value)
    str_temp = str(master_list[0])
    l1 = str_temp.split(",")
    j = 1
    for i in l1:
        par = str(i)
        if (len(par) > 2):
            s1 = str(kite.quote([par]))

            if (par.find("2150000000") != -1):
                  stop_loss(s1)
            l2 = oi_calculation(s1)
            all_oi_ce_temp = 0

            if (j == 1):
                all_oi_ce_temp = (int(float(l2[3]) * (0.98)))
                all_oi_ce_temp = int(all_oi_ce_temp / 1000)
            #  print(l2, all_oi_ce_temp,j)

            if (j < 1 and j > 0):
                all_oi_ce_temp = (int(float(l2[3]) * (j)))
                all_oi_ce_temp = int(all_oi_ce_temp / 1000)
            #    print(l2 , all_oi_ce_temp , j)

            if (j < 0):
                all_oi_ce_temp = (int(float(l2[3]) * (0.01)))
                all_oi_ce_temp = int(all_oi_ce_temp / 1000)
                # print(l2, all_oi_ce_temp , j)

            j = j - 0.05
            all_oi_ce = all_oi_ce + all_oi_ce_temp

    str_temp = str(master_list[1])
    l1 = str_temp.split(",")
    j = 0
    for i in l1:
        par = str(i)
        if (len(par) > 2):

            s1 = str(kite.quote([par]))
            l2 = oi_calculation(s1)
            all_oi_pe_temp = 0
            if (j <= 0):
                all_oi_pe_temp = (int(float(l2[3]) * (0.01)))
                all_oi_pe_temp = int(all_oi_pe_temp / 1000)
            # print(l2, all_oi_pe_temp , j)

            if (j > 0):
                all_oi_pe_temp = (int(float(l2[3]) * (j)))
                all_oi_pe_temp = int(all_oi_pe_temp / 1000)
            # print(l2, all_oi_pe_temp , j)

            j = j + 0.05
            all_oi_pe = all_oi_pe + all_oi_pe_temp

    print(all_oi_ce, all_oi_pe)
    oi_data_file(all_oi_ce - prev_day_ce_oi, all_oi_pe - prev_day_pe_oi)
    print((all_oi_ce - prev_day_ce_oi), (all_oi_pe - prev_day_pe_oi))
    all_oi_pe = 0
    all_oi_ce = 0

    time.sleep(5)
