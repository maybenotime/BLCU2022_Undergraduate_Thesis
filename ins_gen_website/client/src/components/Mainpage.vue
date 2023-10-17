<template>
  <div class="dictmain">
    <div class="content-view">
      <div class="top-div">
        <div>
          <div class="top-main-div">
            <img class="main-img" src="~@/assets/文心-02.png" />
            <h1 class="top-title">{{ mainTitleLabel }}</h1>
          </div>
        </div>

        <div class="top-tool-div">
          <el-tabs
            class="el-tabs__item"
            v-model="activeName"
            @tab-click="handleClick"
          >
            <el-tab-pane :label="hanyuBtn" name="cn"></el-tab-pane>
            <el-tab-pane :label="yingyuBtn" name="en"></el-tab-pane>
            <el-tab-pane :label="jinjuBtn" name="lyric"></el-tab-pane>
          </el-tabs>
        </div>
      </div>

      <div class="top-redict-div">
        <div class="ci-div">
          <div class="input-label">{{ ciLabel }}</div>

          <el-input class="input-keywords" v-model="inputci" :placeholder="ciLabelHolder" @keyup.enter.native="Genbutton">
            <el-select v-model="now_choice" slot="append" placeholder="请选择难度风格">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-input>
        </div>

       
        <div class="search-div" @click="Genbutton">
          <i class="el-icon-search"></i>
          <div class="search-label">{{ searchLabel }}</div>
        </div>
      </div>
    
      <div class="result-div">
        <ul class="result-list" style="overflow: auto">
            <show-result :content="result" v-if="ShowOrNot"></show-result>      
            <!-- 显示结果的组件 -->
        </ul>
        <div class="explainWarn-div" v-if="isShawExplainWarnLabel">
          {{ explainWarnLabel }}
        </div>
      </div>

      <div class="empty-div"></div>
    </div>

    <div class="father-div">
      <label class="tool-btn"
        >Copyright ⓒ 2021 BLCU-ICALL,
        <a
          style="color: #00a1b5; text-decoration: none"
          href="http://nlp.csai.tsinghua.edu.cn"
          >THUNLP</a
        ></label
      >
    </div>
  </div>
</template>

<script>
import ShowResult from "./ShowResult.vue";

export default {
    name: 'Mainpage',
    data(){
        return{
            mainTitleLabel: "文心·例句生成",
            activeName: "cn",                   //默认选中汉语标签页
            inputci:'',                         //用户输入的关键词信息            
            hanyuBtn: "中文",                   
            yingyuBtn: "English",
            jinjuBtn:"锦句",
            ciLabel: "关键词",
            ciLabelHolder: "关键词用空格分隔,最多输入四个关键词",
            searchLabel: "生 成",
            current_page:'cn',
            ShowOrNot:false,
            now_choice:'',

            result:[{
                ci:'',
                ju:''
            }],

            options: [{
              value: 'easy',
              label: '简单'
            }, {
              value: 'normal',
              label: '普通'
            }, {
              value: 'hard',
              label: '困难'
            }],
        }
    },
    components:{
        ShowResult            //组件的嵌套
    },
    methods:{
        Genbutton(){
            var sentence = this.inputci;
            var prompt = this.now_choice;
            var sentence_onespace = sentence.replace(/\s+/g," ");       //去除多余空格
            var keys_list = sentence_onespace.split(" ");    
            var data_post = new FormData();                           //打包成表单数据         
            for(var i=0;i<keys_list.length;i++){
                var key = keys_list[i].trim();
                data_post.append('keywords',key);
            }
            data_post.append('prompt',prompt);
            if(this.current_page == "cn"){
              var targeturl = '/CNsengen'
            }
            else if(this.current_page == "en"){
              var targeturl = '/ENsengen'
            }
            else if(this.current_page == "lyric"){
              var targeturl = '/CNlyric'
            }
            this.ShowOrNot = true;
            this.$axios.post(targeturl,data_post)
            .then((data)=> {                    //使用箭头函数，在then中的操作才会反映到全局
                var str = keys_list.toString();
                this.result[0].ci = str;
                this.result[0].ju = data.data;
            })
            .catch(function (error) {
                console.log(error);
            });
        },

        changepage(page) {                                          //刷新界面
            this.inputci = "";
            this.ShowOrNot = false;
            if (page == "en") {
                (this.ciLabel = "KeyWords"),
                (this.ciLabelHolder = "Split keywords with space"),
                (this.searchLabel = "Generate")
            } else if(page == "cn"){
                (this.ciLabel = "关键词"),
                (this.ciLabelHolder = "关键词用空格分隔"),
                (this.searchLabel = "生成")
            }else {
                (this.ciLabel = "关键词"),
                (this.ciLabelHolder = "关键词用空格分隔"),
                (this.searchLabel = "生成")
            }
        },

        handleClick() {
            if (this.activeName == "cn") {
              this.current_page = "cn";
              this.changepage(this.current_page);       
            } else if (this.activeName == "en") {
              this.current_page = "en";
              this.changepage(this.current_page);
            } else if (this.activeName == "lyric") {
              this.current_page = "lyric";
              this.changepage(this.current_page);
            }
        },
    }
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style scoped>
.el-select {
    width: 180px;
  }
.dictmain {
  margin-top: 0px;
}
label {
  color: #00a1b5;
  font-size: 18px;
  font-weight: bold;
}

.top-div {
  background-color: #f8fcfc;
  height: 160px;
}

.top-main-div {
  width: 700px;
  height: 120px;
  display: flex;
  margin: auto;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.main-img {
  margin: 0px 10px 0 50px;
  width: 60px;
  height: 60px;
}

.top-title {
  margin: 0px 40px 0 0px;
  color: black;
  font-size: 48px;
  font-family: "Times New Roman", "华文中宋";
}

.top-tool-div {
  margin: 0 30px 0;
  display: flex;
}

.top-redict-div {
  margin: 60px 20px 0;
}

.father-div {
  height: 25px;
}

.tool-btn {
  margin: 0px 0px 0px;
  height: 40px;
  width: 70px;
  line-height: 40px;
  text-align: center;
  font-size: 14px;
  font-family: "Arial";
}

.top-result {
  margin: 20px 10px 0 0;
}

.redict-zi {
  position: absolute;
  right: 105px;
  font-size: 14px;
  width: 25px;
  height: 25px;
  text-align: center;
  line-height: 25px;
  border-radius: 17px;
  border: 2px solid #00a1b5;
  font-family: "微软雅黑";
}

.top-one {
  position: absolute;
  top: 70px;
  width: 120px;
  height: 30px;
  line-height: 30px;
  text-align: right;
  right: 150px;
  font-size: 14px;
  color: #333333;
  font-family: "微软雅黑";
}

.top-mid {
  position: absolute;
  background-color: #333333;
  top: 75px;
  width: 3px;
  height: 20px;
  line-height: 30px;
  right: 125px;
  font-size: 20px;
}

.top-two {
  position: absolute;
  top: 70px;
  height: 30px;
  line-height: 30px;
  right: 20px;
  text-align: right;
  font-size: 14px;
  color: #333333;
  font-family: "微软雅黑";
}

.redict-btn {
  position: absolute;
  height: 35px;
  line-height: 0;
  right: 20px;
  font-size: 16px;
  color: #00a0b4;
  border-radius: 10px;
  border: 2px solid #00a0b4;
  font-family: "微软雅黑";
}

.redict-btn:hover {
  background-color: #00a0b4;
  color: white;
}

.input-label {
  margin: 15px 0px 0px 10px;
  width: 120px;
  height: 30px;
  line-height: 30px;
  font-size: 18px;
  color: #333333;
  border-right: 2px solid #00a0b4;
  font-family: "微软雅黑";
}

.ci-div {
  display: flex;
  margin: 0 30px 0 30px;
  border-radius: 15px;
  border: 1px solid #00a1b5;
}

.ci-div >>> .el-input__inner {
  border: 0;
}

.input-keywords {
  margin: 10px 10px 10px 10px;
  font-size: 18px;
}

.ju-div >>> .el-input__inner {
  border: 0;
}

.input-ju {
  margin: 10px 10px 10px 10px;
  font-size: 18px;
}

.search-div {
  display: flex;
  width: 400px;
  background-color: #00a0b4;
  border-radius: 10px;
  margin: auto;
  margin-top: 30px;
  cursor: pointer;
}

.el-icon-search {
  margin: 10px 10px 0 160px;
  font-size: 20px;
  color: white;
  font-weight: bold;
}
.search-label {
  margin: 7px 0px 10px 00px;
  font-size: 18px;
  color: white;
  font-weight: bold;
  font-family: "微软雅黑";
}

.search-btn {
  width: 190px;
}
</style>

