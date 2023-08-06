import matplotlib.pyplot as plt 

class ImageProcessing():

    def __init__ (self, image_path):
        """builder to load the image location in the directory"""

        self.image_path = image_path
        
        return None
    
    def image_array(self):
        """turns the image into a numpy array"""

        image_object = plt.imread(self.image_path)

        return image_object

    def benford_law(self, image_array):
        """calculates a list of probability of the frequency of digits according to benford's law"""
        
        one, two, three, four, five, six, seven, eight, nine = 0, 0, 0, 0, 0, 0, 0, 0, 0
        for values in image_array.flatten():
            if str(values)[0] == '1':
                one += 1
            elif str(values)[0] == '2':
                two += 1
            elif str(values)[0] == '3':
                three += 1
            elif str(values)[0] == '4':
                four += 1
            elif str(values)[0] == '5':
                five += 1
            elif str(values)[0] == '6':
                six += 1
            elif str(values)[0] == '7':
                seven += 1
            elif str(values)[0] == '8':
                eight += 1
            elif str(values)[0] == '9':
                nine += 1
        list_prob = []
        list_prob.append(one / image_array.flatten().size)
        list_prob.append(two / image_array.flatten().size)
        list_prob.append(three / image_array.flatten().size)
        list_prob.append(four / image_array.flatten().size)
        list_prob.append(five / image_array.flatten().size)
        list_prob.append(six / image_array.flatten().size)
        list_prob.append(seven / image_array.flatten().size)
        list_prob.append(eight / image_array.flatten().size)
        list_prob.append(nine / image_array.flatten().size)

        return list_prob