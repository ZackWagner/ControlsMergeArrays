#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

class MergeArrays(Node):

    def __init__(self):
        super().__init__("merge_arrays_node")
        self.subscription1 = self.create_subscription(
            Int32MultiArray, "/input/array1", self.array1_callback, 10)
        self.subscription1 = self.create_subscription(
            Int32MultiArray, "/input/array2", self.array2_callback, 10)
        self.array1 = None
        self.array2 = None
        self.finalarray = []
        self.pub = self.create_publisher(
            Int32MultiArray,
            '/output/array',
            10
        )
        self.get_logger().info("This will eventually merge arrays")

    # Callback method for when /input/array1 recieved
    def array1_callback(self, msg: Int32MultiArray):
        self.array1 = msg.data
        if self.array2 is not None: # Have both arrays, merge
            self.merge_arrays(self.array1, self.array2)
            self.array1 = None
            self.array2 = None

        
    # Callback method for when /input/array2 recieved
    def array2_callback(self, msg: Int32MultiArray):
        self.array2 = msg.data
        if self.array1 is not None: # Have both arrays, merge
            self.merge_arrays(self.array1, self.array2)
            self.array1 = None
            self.array2 = None
            return

    # Method for publishing the array to /output/array
    def send_merged_array(self):
        msg = Int32MultiArray()
        msg.data = self.finalarray
        self.pub.publish(msg)
        self.finalarray.clear()



    # This method contains the array merging algorithm given two sorted arrays
    # it returns a sorted array with all the values in both arrays O(N+M)
    def merge_arrays(self, arr1: list, arr2: list):

        idx1 = 0
        idx2 = 0
        result = []
        while idx1 < len(arr1) or idx2 < len(arr2):
             # Iterate through both arrays, each step adding the min of each array to the merged array
            if idx1 < len(arr1) and idx2 < len(arr2):
                self.finalarray.append(min(arr1[idx1], arr2[idx2]))
                if min(arr1[idx1], arr2[idx2]) == arr1[idx1]:
                    idx1 = idx1+1
                else:
                    idx2 = idx2+1
            else:
                if idx1 < len(arr1): 
                    self.finalarray.append(arr1[idx1])
                    idx1 = idx1+1
                else:
                    self.finalarray.append(arr2[idx2])
                    idx2 = idx2+1
        
        self.send_merged_array() # Publish merged array
        

# Main driver method to create and spin the node
def main(args=None):
    
    rclpy.init(args=args)

    node = MergeArrays()

    rclpy.spin(node)

    rclpy.shutdown()
