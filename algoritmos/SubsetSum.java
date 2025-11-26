package algoritmos;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;

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
        int target = Integer.parseInt(args[0]);

        String path = args[1];
        List<Integer> list = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            String json = br.readLine();
            json = json.replace("[", "").replace("]", "");
            String[] parts = json.split(",");

            for (String p : parts) {
                if (!p.isBlank()) {
                    list.add(Integer.parseInt(p.trim()));
                }
            }
        }

        int[] arr = list.stream().mapToInt(i -> i).toArray();

        subsetSum(arr, target);
    }
}
