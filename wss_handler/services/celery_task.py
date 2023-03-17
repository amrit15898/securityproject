from celery import shared_task


@shared_task(bind=True)
def connect_natsat_wss_celery_task(self,):
    print("here")
    # connect_to_deal()
    return "connection done"
