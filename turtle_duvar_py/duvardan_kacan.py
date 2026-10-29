#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose


class DuvardanKacanNode(Node):
    def __init__(self):
        super().__init__('duvardan_kacan')

        # Bonus: Hız ve sınır değerlerini parametre olarak tanımlama
        self.declare_parameter('linear_speed', 2.2)
        self.declare_parameter('angular_speed', 2.6)
        self.declare_parameter('min_limit', 1.0)
        self.declare_parameter('max_limit', 10.0)

        # Yayıncı: /turtle1/cmd_vel konusuna hız mesajı gönderir
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # Abone: /turtle1/pose konusunu dinleyip x ve y değerlerini alır
        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.current_pose = None

        # Log: Konumu saniyede bir get_logger().info() ile yazdırır
        self.log_timer = self.create_timer(1.0, self.log_timer_callback)

        self.get_logger().info('Duvardan kacan kaplumbaga dugumu aktif edildi.')

    def pose_callback(self, msg: Pose):
        self.current_pose = msg

        linear_speed = self.get_parameter('linear_speed').get_parameter_value().double_value
        angular_speed = self.get_parameter('angular_speed').get_parameter_value().double_value
        min_limit = self.get_parameter('min_limit').get_parameter_value().double_value
        max_limit = self.get_parameter('max_limit').get_parameter_value().double_value

        cmd = Twist()

        # x veya y 1.0'dan küçük ya da 10.0'dan büyükse dönerek yön değiştirsin
        if (msg.x < min_limit or msg.x > max_limit or
                msg.y < min_limit or msg.y > max_limit):
            cmd.linear.x = linear_speed * 0.45
            cmd.angular.z = angular_speed
        else:
            cmd.linear.x = linear_speed
            cmd.angular.z = 0.0

        self.cmd_vel_pub.publish(cmd)

    def log_timer_callback(self):
        if self.current_pose is not None:
            min_limit = self.get_parameter('min_limit').get_parameter_value().double_value
            max_limit = self.get_parameter('max_limit').get_parameter_value().double_value
            sinirda = (
                self.current_pose.x < min_limit or self.current_pose.x > max_limit or
                self.current_pose.y < min_limit or self.current_pose.y > max_limit
            )
            durum_metni = 'Sinir asildi -> Donus yapiliyor' if sinirda else 'Guvenli bolgede ilerliyor'
            self.get_logger().info(
                f'Anlik Konum [x: {self.current_pose.x:.2f}, y: {self.current_pose.y:.2f}] - {durum_metni}'
            )


def main(args=None):
    rclpy.init(args=args)
    node = DuvardanKacanNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
