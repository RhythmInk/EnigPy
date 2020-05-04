##############
#List Methods#
##############


def cycle_list(lst,n=1):
    for i in range(n):
        #create temporary value to store last elt in list
        temp = lst[-1]
        n = len(lst)-1

        #move nth elt to n+1 position
        for i in range(n):
                lst[n-i]=lst[n-(i+1)]

        #set 0th elt to be temp
        lst[0] = temp

    return lst


def reverse_cycle_list(lst,n=1):
    #create temporary value to store first elt in list
    for i in range(n):
        temp = lst[0]
        n = len(lst)-1
        #move nth elt to n+1 position save for the last
        for i in range(n):
                lst[i]=lst[i+1]
        #set last elt to be temp
        lst[-1] = temp

    return lst


def exchange_index_pos(lst):
    '''
    Only works for lists who contain elements less than their length
    Lists must contain positive integers
    '''
    temp = [0] * len(lst)

    for i, j in enumerate(lst): #enum[1,2] = [(0,1), (1,2)]
        temp[j] = i

    return temp

