import { Flex, Icon, Link } from '@chakra-ui/react'
import { useColorModeValue } from 'components/ui/color-mode'
import { NavItemProps } from '../types'

export const NavItem = ({ icon, children, path, ...rest }: NavItemProps) => {
	const hoverBg = useColorModeValue('cyan.400', 'cyan.600')
	const hoverColor = useColorModeValue('white', 'gray.100')

	return (
		<Flex
			align='center'
			p='4'
			mx='4'
			borderRadius='lg'
			cursor='pointer'
			_hover={{
				bg: hoverBg,
				color: hoverColor
			}}
			w='100%'
			{...rest}
		>
			<Link
				href={path || '#'}
				_hover={{ textDecoration: 'none' }}
				_focus={{ boxShadow: 'none' }}
				h='100%'
			>
				<Icon mr='4' fontSize='16' as={icon} />
				{children}
			</Link>
		</Flex>
	)
}
