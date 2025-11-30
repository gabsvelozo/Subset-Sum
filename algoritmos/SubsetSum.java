package algoritmos;

import java.util.Random;

public class SubsetSum {

    public static boolean subsetSum(int[] arr, int target) {
        boolean[] dp = new boolean[target + 1];
        dp[0] = true;

        for (int num : arr) {
            for (int j = target; j >= num; j--) {
                dp[j] = dp[j] || dp[j - num];
            }
        }

        return dp[target];
    }

    public static void main(String[] args) throws Exception {
        int size = Integer.parseInt(args[0]);
        int target = Integer.parseInt(args[1]);

        Random r = new Random();
        int[] arr = new int[size];

        for (int i = 0; i < size; i++) {
            arr[i] = r.nextInt(size) + 1;
        }

        subsetSum(arr, target);
    }
}
