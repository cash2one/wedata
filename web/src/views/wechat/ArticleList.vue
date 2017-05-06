<template>
	<section>

		<!--列表-->
		<el-table :data="items" highlight-current-row v-loading="listLoading" :stripe="true" @selection-change="handleSelectionChange" style="width: 100%;">
			<el-table-column type="selection" width="55">
			</el-table-column>
			<el-table-column prop="account_id" label="公众号id" sortable>
			</el-table-column>
			<el-table-column prop="article_title" label="文章标题" sortable>
			</el-table-column>
			<el-table-column prop="author" label="作者" sortable>
			</el-table-column>
			</el-table-column>
			<el-table-column label="操作" width="260">
				<template scope="scope">
					<!-- <el-button size="small" @click="handleRun">启动</el-button> -->
					<!-- <el-button size="small" @click="handleEdit(scope.$index, scope.row)">配置</el-button>
					<el-button size="small" @click="handleScriptEdit(scope.$index, scope.row)">规则</el-button>
					<el-button size="small" @click="openTaskList(scope.$index, scope.row)">任务</el-button>
					<el-button size="small" @click="openProjectTest(scope.$index, scope.row)">Test</el-button> -->
				</template>
			</el-table-column>
		</el-table>

		<!--工具条-->
		<el-col :span="24" class="toolbar">
			<el-pagination layout="prev, pager, next" @current-change="handleCurrentChange" :page-size="page_size" :total="total" style="float:right;">
			</el-pagination>
		</el-col>
	</section>
</template>


<script>
	import util from '../../common/js/util'
	import NProgress from 'nprogress'
	import { getArticleList } from '../../api/api'
	export default {
		data() {
			return {
				total: 0,
				page: 1,
				page_size: 15,
				items: [],
				listLoading: false,

				sels: [],//列表选中列
			}
		},
		methods: {
			getArticles() {
				let params = {
					page: this.page,
					page_size: this.page_size,
				}
				this.listLoading = true;
				getArticleList(this.$route.params.name, params).then((res) => {
					this.total = res.data.total
					this.items = res.data.results;
					this.listLoading = false;
				})
			},

			handleCurrentChange(val) {
				this.page = val;
				this.getArticles();
			},
			handleSelectionChange: function (sels) {
				this.sels = sels;
			},
		},
		mounted() {
			this.getArticles();
		}
	}

</script>

<style scoped>

</style>
