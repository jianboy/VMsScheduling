package me.yoqi.servermanager;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.google.common.base.Charsets;

/**默认不迁移，初始代码。跑a数据分数6148
 * Created by mou.sunm on 2018/07/02.
 */
public class Main2 {
	// 参数
	public static final double alpha = 10.;
	public static final double beta = 0.5;
	public static final int T = 98;
	public static final int EXEC_LIMIT = 100000;

	// 静态数据
	private int num_app; // app数 9338
	private int num_inst; // inst数 68219
	private int num_mac; // machine数 6000
	private int num_k; // 资源种类 200
	private List<Integer> cpuIter; // [0, 1, 2, ... 97]
	private Map<String, Integer> appIndex; // app_1,app_2字符串用0,1等数字替换，{app_1=0,
											// app_2=1,...,app_4=3}
	private Map<String, Integer> machineIndex;// {machine_1=0, machine_2=1,
	private List<Integer> machinePriorIndex=new ArrayList<Integer>();
	private String[] apps; // [app_1, app_2, app_3, app_4,
	private String[] machines;// [machine_1, machine_2, machine_3, machine_4,
	private Map<String, Integer> inst2AppIndex;// {inst_157=49}

	private double[][] appResources;// app 9338*200
	private double[][] machineResources;// 主机 6000*200
	private Map<Integer, Integer>[] appInterference;// 9338 限制条件[{}, {},
													// {3517=2}, {}, {5600=1,
													// 6747=2, 7707=2, 4830=2},

	// 动态数据
	private Map<String, Integer> inst2Machine;// 部署 {inst_33717=5456,
	// 这个数据类型和Map<String, Integer>有点区别，加上list会保存顺序
	private List<String> deployResult = new ArrayList<String>(); // [inst_33717,5456
	private List<String> instUnDelpoy = new ArrayList<String>();// 未部署的实例
	private Map<String, Integer> inst2MachineDefaultConflict = new HashMap<String, Integer>();;// 记录初始部署冲突的实例和主机
	private double[][] machineResourcesUsed;// 6000*200
	private Map<Integer, Integer>[] machineHasApp;// 6000 [{}, {},{6004=1,
													// 9126=1, 1598=1}, {}, {},
													// {},

	/**
	 * 先对disk排序，然后first fit
	 * 
	 * @throws IOException
	 *             写文件异常
	 */
	private void run() throws IOException {
//		主机优先顺序，使用过的主机在前，目的紧凑；然后大主机在前。做一个主机优先部署序列
		
		
		// 对默认实例有冲突的进行迁移
		String tmp_Res;
		String inst_tmp = null;
		int machineIt_tmp = 0;
		for (Map.Entry<String, Integer> entry : inst2MachineDefaultConflict.entrySet()) {
			// 将实例先迁移出来，释放资源
			pickInstance(entry.getKey());
			for (Map.Entry<String, Integer> entry2 : machineIndex.entrySet()) {
				inst_tmp = entry.getKey();
				machineIt_tmp = entry2.getValue();
				tmp_Res = toMachine(inst_tmp, machineIt_tmp);
				if (tmp_Res == "success") {
					deployResult.add(inst_tmp + "," + "machine_" + (machineIt_tmp + 1));
					break;
				}
			}
		}
		System.out.println("默认冲突数：" + inst2MachineDefaultConflict.size());
		System.out.println("剩余未部署：" + instUnDelpoy.size());
		//对剩余未部署的实例进行部署

		for (int i = 0; i < instUnDelpoy.size(); i++) {
			for (Map.Entry<String, Integer> entry2 : machineIndex.entrySet()) {
				inst_tmp = instUnDelpoy.get(i);
				machineIt_tmp = entry2.getValue();
				tmp_Res = toMachine(inst_tmp, machineIt_tmp);
				if (tmp_Res == "success") {
					deployResult.add(inst_tmp + "," + "machine_" + (machineIt_tmp + 1));
					break;
				}
			}
		}
		saveResult(deployResult);
	}

	private void sortInstanceByDisk(ArrayList<Integer> instance) {
		for (int i = 0; i < instance.size(); i++) {
			inst2AppIndex.get(i);
		}
	}

	private void sort(ArrayList<Integer> list) {

	}

	// 读取数据
	protected void init(BufferedReader bufferedReader) throws IOException {
		cpuIter = new ArrayList<Integer>();
		for (int i = 0; i < T; i++)
			cpuIter.add(i);
		/** Read app_resources */
		num_app = Integer.parseInt(bufferedReader.readLine());// 9338
		apps = new String[num_app];
		for (int i = 0; i < num_app; i++) {// 循环app表每一行
			// appId,resources
			String line = bufferedReader.readLine();
			String[] parts = line.split(",", -1);
			List<Double> resources = new ArrayList<Double>();
			for (String x : parts[1].split("\\|", -1))// cpu
				resources.add(Double.parseDouble(x));
			for (String x : parts[2].split("\\|", -1))// mem
				resources.add(Double.parseDouble(x));
			for (int j = 3; j < parts.length; j++) // disk/P/M/PM
				resources.add(Double.parseDouble(parts[j]));
			if (i == 0) {
				num_k = resources.size();
				appIndex = new HashMap<String, Integer>();
				appResources = new double[num_app][num_k];
			}
			if (num_k != resources.size())
				throw new IOException("[DEBUG 2]Invaild problem");
			if (appIndex.containsKey(parts[0]))
				throw new IOException("[DEBUG 3]Invaild problem");
			appIndex.put(parts[0], i);
			apps[i] = parts[0];// [app_1, app_2, app_3, app_4]
			for (int j = 0; j < num_k; j++)
				appResources[i][j] = resources.get(j);
		}
		/** Read machine_resources */
		num_mac = Integer.parseInt(bufferedReader.readLine());// 6000
		machineResources = new double[num_mac][num_k];
		machineResourcesUsed = new double[num_mac][num_k];
		machineIndex = new HashMap<String, Integer>();// {machine_3791=3790,
		machineHasApp = new Map[num_mac];
		machines = new String[num_mac];
		for (int i = 0; i < num_mac; i++) {
			// machineId,resources
			String line = bufferedReader.readLine();
			String[] parts = line.split(",", -1);
			if (machineIndex.containsKey(parts[0]))
				throw new IOException("[DEBUG 4]Invaild problem");
			machineIndex.put(parts[0], i);
			machines[i] = parts[0];
			machineHasApp[i] = new HashMap<Integer, Integer>();
			double cpu = Double.parseDouble(parts[1]);
			double mem = Double.parseDouble(parts[2]);
			for (int j = 0; j < T; j++) {
				machineResources[i][j] = cpu;
				machineResources[i][T + j] = mem;
			}
			for (int j = 3; j < parts.length; j++)
				machineResources[i][2 * T + j - 3] = Double.parseDouble(parts[j]);
			for (int j = 0; j < num_k; j++)
				machineResourcesUsed[i][j] = 0.;

		}
		// // 倒序排列，大主机在前面
		// List<Map.Entry<String, Integer>> list_tmp = new ArrayList<>();
		// for (Map.Entry<String, Integer> entry : machineIndex.entrySet()) {
		// list_tmp.add(entry); // 将map中的元素放入list中
		// }
		// list_tmp.sort(new Comparator<Map.Entry<String, Integer>>() {
		// @Override
		// public int compare(Map.Entry<String, Integer> o1, Map.Entry<String,
		// Integer> o2) {
		// return o2.getValue() - o1.getValue();
		// }
		// // 逆序（从大到小）排列，正序为“return o1.getValue()-o2.getValue”
		// });
		// machineIndex.clear();
		// for (Map.Entry<String, Integer> entry : list_tmp) {
		// machineIndex.put(entry.getKey(), entry.getValue());
		// }
		/** Read app_interference */
		int icnt = Integer.parseInt(bufferedReader.readLine());// 35242
		appInterference = new Map[num_app];
		for (int i = 0; i < num_app; i++)
			appInterference[i] = new HashMap<Integer, Integer>();
		for (int i = 0; i < icnt; i++) {
			String line = bufferedReader.readLine();
			String[] parts = line.split(",", -1);
			if (!appIndex.containsKey(parts[0]) || !appIndex.containsKey(parts[1]))
				throw new IOException("[DEBUG 8]Invaild problem");
			int app1 = appIndex.get(parts[0]);
			int app2 = appIndex.get(parts[1]);
			int limit = Integer.parseInt(parts[2]);
			Map<Integer, Integer> inter = appInterference[app1];
			if (inter.containsKey(app2))
				throw new IOException("[DEBUG 9]Invaild problem");
			if (app1 == app2)
				limit += 1; // self-interference +1 here
			inter.put(app2, limit);
		}
		/** Read instance_deploy */
		num_inst = Integer.parseInt(bufferedReader.readLine());// 68219
		inst2AppIndex = new HashMap<String, Integer>();// 68219*2
														// {inst_33717=8766,
														// inst_33718=2956}
		inst2Machine = new HashMap<String, Integer>();// {inst_33717=5456,
		for (int i = 0; i < num_inst; i++) {
			String line = bufferedReader.readLine();
			String[] parts = line.split(",", -1);
			if (inst2AppIndex.containsKey(parts[0]))
				throw new IOException("[DEBUG 5]Invaild problem");
			if (!appIndex.containsKey(parts[1]))
				throw new IOException("[DEBUG 6]Invaild problem");
			inst2AppIndex.put(parts[0], appIndex.get(parts[1]));
			if (!"".equals(parts[2])) {
				if (!machineIndex.containsKey(parts[2]))
					throw new IOException("[DEBUG 7]Invaild problem");
				toMachineDefault(parts[0], machineIndex.get(parts[2]));
			} else {
				instUnDelpoy.add(parts[0]);
			}
		}
		System.out.println("finish init");
	}

	private String toMachineDefault(String inst, int machineIt) {
		int appIt = inst2AppIndex.get(inst);
		Map<Integer, Integer> hasApp = machineHasApp[machineIt];
		String res_tmp = doCheck(inst, machineIt);
		if (res_tmp != "success") {
			inst2MachineDefaultConflict.put(inst, machineIt);
		}
		// 将inst放入新的machine
		inst2Machine.put(inst, machineIt);
		if (!hasApp.containsKey(appIt))
			hasApp.put(appIt, 0);
		hasApp.put(appIt, hasApp.get(appIt) + 1);
		for (int i = 0; i < num_k; i++)
			machineResourcesUsed[machineIt][i] += appResources[appIt][i];

		return "success";
	}

	private String toMachine(String inst, int machineIt) {
		return toMachine(inst, machineIt, true);
	}

	private String doCheck(String inst, int machineIt) {
		int appIt = inst2AppIndex.get(inst);
		Map<Integer, Integer> hasApp = machineHasApp[machineIt];
		// 检查互斥规则，初始数据这里有冲突
		int nowHas = 0;
		if (hasApp.containsKey(appIt))
			nowHas = hasApp.get(appIt);
		for (Integer conditionalApp : hasApp.keySet()) {
			if (hasApp.get(conditionalApp) <= 0)
				continue;
			if (!appInterference[conditionalApp].containsKey(appIt))
				continue;
			if (nowHas + 1 > appInterference[conditionalApp].get(appIt)) {
				return "App Interference, inst: " + inst + ", " + apps[conditionalApp] + " -> " + apps[appIt] + ", "
						+ (nowHas + 1) + " > " + appInterference[conditionalApp].get(appIt);
			}
		}
		// 初始数据这里有冲突
		for (Integer checkApp : hasApp.keySet()) {
			if (!appInterference[appIt].containsKey(checkApp))
				continue;
			if (hasApp.get(checkApp) > appInterference[appIt].get(checkApp)) {
				return "App Interference, inst: " + inst + ", " + apps[appIt] + " -> " + apps[checkApp] + ", "
						+ (nowHas + 1) + " > " + appInterference[appIt].get(checkApp);
			}
		}
		// 检查资源限制，初始数据这里没有冲突
		for (int i = 0; i < num_k; i++)
			if (dcmp(
					machineResourcesUsed[machineIt][i] + appResources[appIt][i] - machineResources[machineIt][i]) > 0) {
				String res = "Resource Limit: inst: " + inst + ", " + "machine: " + machines[machineIt] + ", app: "
						+ apps[appIt] + ", resIter: " + i + ", " + machineResourcesUsed[machineIt][i] + " + "
						+ appResources[appIt][i] + " > " + machineResources[machineIt][i];
				// System.out.println(res);
				return res;
			}

		return "success";
	}

	private String toMachine(String inst, int machineIt, boolean doCheck) {
		int appIt = inst2AppIndex.get(inst);
		Map<Integer, Integer> hasApp = machineHasApp[machineIt];
		if (doCheck) {
			String res_tmp = doCheck(inst, machineIt);
			if (res_tmp != "success") {
				return res_tmp;
			}
		}
		// 将inst放入新的machine
		inst2Machine.put(inst, machineIt);
		if (!hasApp.containsKey(appIt))
			hasApp.put(appIt, 0);
		hasApp.put(appIt, hasApp.get(appIt) + 1);
		for (int i = 0; i < num_k; i++)
			machineResourcesUsed[machineIt][i] += appResources[appIt][i];

		return "success";
	}

	/**
	 * 把实例inst 移除主机，撤销消耗资源
	 * 
	 * @param inst
	 *            实例id
	 */
	private void pickInstance(String inst) {
		if (!inst2Machine.containsKey(inst))
			return;
		int appIt = inst2AppIndex.get(inst);
		int fromMachine = inst2Machine.get(inst);
		// 更新machineHasApp
		Map<Integer, Integer> fromHasApp = machineHasApp[fromMachine];
		fromHasApp.put(appIt, fromHasApp.get(appIt) - 1);
		if (fromHasApp.get(appIt) <= 0)
			fromHasApp.remove(appIt);
		// 更新machineResourcesUsed
		for (int i = 0; i < num_k; i++)
			machineResourcesUsed[fromMachine][i] -= appResources[appIt][i];
		// 更新inst2Machine
		inst2Machine.remove(inst);
	}

	private int dcmp(double x) {
		if (Math.abs(x) < 1e-9)
			return 0;
		return x < 0. ? -1 : 1;
	}

	private void saveResult(List<String> res) throws IOException {
		String res_path = "result.csv";
		File file = new File(res_path);
		if (!file.exists()) {
			file.createNewFile();
		}
		BufferedWriter writer = new BufferedWriter(new FileWriter(file));
		for (int i = 0; i < res.size(); i++) {
			writer.write(res.get(i));
			writer.newLine();
		}
		// for (String line : res) {
		// writer.write(line);
		// writer.newLine();
		// }
		writer.close();
	}

	public static void main(String[] args) throws Exception {
		if (args.length != 4 && args.length != 2) {
			System.err.println(
					"传入参数有误，使用方式为：java -cp xxx.jar  app_resources.csv machine_resources.csv instance_deploy.csv app_interference.csv");
			return;
		}

		System.out.println("-------开始部署啦--------");
		long startTime = System.currentTimeMillis(); // 获取开始时间

		InputStream problem;
		// app_resources.csv
		// machine_resources.csv
		// instance_deploy.csv
		// app_interference.csv
		if (args.length == 4) {
			// 将赛题拼成评测数据
			StringBuffer sb = new StringBuffer();
			for (int i = 0; i < 4; i++) {
				List<String> lines = new ArrayList<String>();
				BufferedReader bs = new BufferedReader(new FileReader(new File(args[i])));
				for (String line = bs.readLine(); line != null; line = bs.readLine())
					lines.add(line);
				sb.append("" + lines.size()).append("\n");
				for (String line : lines)
					sb.append(line).append("\n");
			}
			String alldata = sb.toString();
			problem = new ByteArrayInputStream(alldata.getBytes());
		} else {
			problem = new FileInputStream(args[0]);
		}

		// 评测
		Main2 evaluator = new Main2();
		evaluator.init(new BufferedReader(new InputStreamReader(problem, Charsets.UTF_8)));
		System.out.println("默认已经部署了：" + evaluator.inst2Machine.size());
		evaluator.run();

		long endTime = System.currentTimeMillis(); // 获取结束时间
		System.out.println("程序运行时间：" + (endTime - startTime) / 1000 + "s"); // 输出程序运行时间
		System.out.println("-------部署结束啦--------");
	}

}
