import csv
from django.core.management.base import BaseCommand
from ORDER.models import OrderItem  
from django.utils import timezone

class Command(BaseCommand):
    help = 'Export order items to CSV file'

    def handle(self, *args, **kwargs):
        # Tên file xuất ra
        current_time = timezone.now().strftime("%Y%m%d_%H%M%S")
        filename = f'order_items_{current_time}.csv'
        
        # Lấy tất cả order items
        order_items = OrderItem.objects.all()

        # Mở file CSV và ghi dữ liệu
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Order ID', 'User', 'Shoe', 'Size', 'Created At']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in order_items:
                writer.writerow({
                    'Order ID': item.order.id,
                    'User': item.order.user.username,
                    'Shoe': item.shoe.name,
                    'Size': item.size.name,
                    'Created At': item.order.created_at,
                })

        self.stdout.write(self.style.SUCCESS(f'Successfully exported {order_items.count()} items to {filename}'))
