from django.shortcuts import render, redirect
from .models import Operation

def calculator_view(request):
    result = None
    history = Operation.objects.all().order_by('-created_at')[:10]  # Ласт 10 операций

    if request.method == "POST":
        try:
            num1 = float(request.POST.get("num1"))
            num2 = float(request.POST.get("num2"))
            operation = request.POST.get("operation")

            # Выполнение операций
            if operation == "add":
                result = num1 + num2
                operation_text = f"{num1} + {num2}"
            elif operation == "subtract":
                result = num1 - num2
                operation_text = f"{num1} - {num2}"
            elif operation == "multiply":
                result = num1 * num2
                operation_text = f"{num1} × {num2}"
            elif operation == "divide":
                result = num1 / num2 if num2 != 0 else "На ноль делить нельзя!"
                operation_text = f"{num1} ÷ {num2}"
            elif operation == "power":
                result = num1 ** num2
                operation_text = f"{num1} ^ {num2}"
            elif operation == "modulus":
                result = num1 % num2
                operation_text = f"{num1} % {num2}"
            elif operation == "sqrt":
                result = num1 ** (1 / num2)
                operation_text = f"√{num1} (степень {num2})"
            else:
                result = "Неверная операция!"

            # сейв в бд
            Operation.objects.create(operation=operation_text, result=str(result))
        except ValueError:
            result = "Ошибка: введите корректные числа!"

    return render(request, "calculator.html", {"result": result, "history": history})

def clear_history_view(request):
    Operation.objects.all().delete()
    return redirect("/")
