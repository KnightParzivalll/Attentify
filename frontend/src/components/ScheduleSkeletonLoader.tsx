import { Skeleton, Stack } from '@chakra-ui/react'

const ScheduleSkeletonLoader: React.FC = () => (
	<Stack>
		<Skeleton height='20px' />
		<Skeleton height='20px' />
		<Skeleton height='20px' />
	</Stack>
)

export default ScheduleSkeletonLoader
