package gson;

import bean.Person;
import com.google.gson.FieldNamingStrategy;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.lang.reflect.Field;

public class GSONCreateSample {

    public static void main(String[] args) {
        GSONCreateSample();
    }

    private static void GSONCreateSample() {
        Person laowang = new Person();
        laowang.setName("隔壁老王");
        laowang.setAge(25);
        laowang.setBirthday("1990-01-01");
        laowang.setSchool("蓝翔");
        laowang.setMajor(new String[] {"挖掘机", "计算机"});
        laowang.setHas_girlfriend(false);
        laowang.setCar(null);
        laowang.setHouse(null);
        laowang.setComment("这是一个注释");
        laowang.setIgnore("不要看见我");

        // 压缩 null
        Gson gson1 = new Gson();
        System.out.println(gson1.toJson(laowang));
        // 保留 null
        Gson gson2 = new GsonBuilder().serializeNulls().create();
        System.out.println(gson2.toJson(laowang));
        // pretty JSON
        Gson gson3 = new GsonBuilder().setPrettyPrinting().create();
        System.out.println(gson3.toJson(laowang));
        // FieldNaming Strategy
        // 忽略transient关键字
        Gson gson4 = new GsonBuilder().setFieldNamingStrategy(new FieldNamingStrategy() {
            @Override
            public String translateName(Field f) {
                if(f.getName().equals("age"))
                    return "AGE";
                return f.getName();
            }
        }).create();
        System.out.println(gson4.toJson(laowang));
    }
}
