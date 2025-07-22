<bean id="bankOfCommunicationsTask" class="com.jan.base.service.task.BankOfCommunicationsTask">
		<property name="transactionDao" ref="transactionDao"/>
		<property name="payHeaderService" ref="payHeaderService"/>
		<property name="transactionManager" ref="transactionManager" />
</bean>

<bean id="bankExecutePayAgencyJob" class="org.springframework.scheduling.quartz.MethodInvokingJobDetailFactoryBean">
		<property name="targetObject" ref="bankOfCommunicationsTask"/>
		<property name="targetMethod" value="executePayAgency"/>
	</bean>

	<bean id="bankPayAgencyResultJob" class="org.springframework.scheduling.quartz.MethodInvokingJobDetailFactoryBean">
		<property name="targetObject" ref="bankOfCommunicationsTask"/>
		<property name="targetMethod" value="queryPayAgencyResult"/>
	</bean>

<!-- 定时处理bankExecutePayAgencyJob数据 -->
	<bean id="bankExecutePayAgencyJobCronTriggerBean" class="org.springframework.scheduling.quartz.CronTriggerFactoryBean">
		<property name="jobDetail" ref="bankExecutePayAgencyJob"/>
		<!-- 触发时间(使用cron表达式) -->
		<property name="cronExpression">
			<value>0 0/12 * * * ?</value>
		</property>
	</bean>

<!-- 定时处理bankPayAgencyResultJob数据 -->
	<bean id="bankPayAgencyResultJobCronTriggerBean" class="org.springframework.scheduling.quartz.CronTriggerFactoryBean">
		<property name="jobDetail" ref="bankPayAgencyResultJob"/>
		<!-- 触发时间(使用cron表达式) -->
		<property name="cronExpression">
			<value>0 0/12 * * * ?</value>
		</property>
	</bean>

<!-- <ref bean="bankExecutePayAgencyJobCronTriggerBean"/> -->
<!-- <ref bean="bankPayAgencyResultJobCronTriggerBean"/> -->
